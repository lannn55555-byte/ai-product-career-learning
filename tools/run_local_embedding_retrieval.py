#!/usr/bin/env python3
"""Build local BGE-M3 embeddings and evaluate dense retrieval for the Agent RAG.

The script intentionally uses no API.  It encodes the approved local corpus once,
stores the vectors locally, then retrieves against the acceptance set with cosine
similarity.  Stage metadata is applied before ranking, just as it will be in the
Agent.  The resulting report is comparable with the keyword-baseline report.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


DEFAULT_MODEL = "BAAI/bge-m3"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunks", required=True, type=Path)
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--gold-standard", type=Path)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--model-cache", required=True, type=Path)
    parser.add_argument("--embeddings-output", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--device", default="cpu")
    parser.add_argument(
        "--reuse-embeddings",
        action="store_true",
        help="Reuse an existing embedding matrix when its row count matches the corpus.",
    )
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def corpus_fingerprint(chunks: list[dict]) -> str:
    digest = hashlib.sha256()
    for chunk in chunks:
        digest.update(chunk["chunk_id"].encode("utf-8"))
        digest.update(b"\0")
        digest.update(chunk["retrieval_text"].encode("utf-8"))
        digest.update(b"\0")
    return digest.hexdigest()


def hint_matches(path: str, hint: str) -> bool:
    return path.startswith(hint) if hint.endswith("/") else path == hint


def load_or_build_embeddings(
    model: SentenceTransformer,
    chunks: list[dict],
    destination: Path,
    metadata_destination: Path,
    batch_size: int,
    reuse: bool,
    fingerprint: str,
    model_name: str,
) -> tuple[np.ndarray, bool]:
    if reuse and destination.exists() and metadata_destination.exists():
        embeddings = np.load(destination)
        metadata = json.loads(metadata_destination.read_text(encoding="utf-8"))
        if (
            embeddings.shape[0] == len(chunks)
            and metadata.get("corpus_fingerprint") == fingerprint
            and metadata.get("model") == model_name
        ):
            return embeddings, True
        print(
            "Existing embedding matrix does not match this corpus fingerprint or model. Rebuilding.",
            file=sys.stderr,
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    texts = [chunk["retrieval_text"] for chunk in chunks]
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    np.save(destination, embeddings)
    metadata_destination.write_text(
        json.dumps(
            {
                "model": model_name,
                "corpus_fingerprint": fingerprint,
                "chunk_count": len(chunks),
                "dimensions": int(embeddings.shape[1]),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return embeddings, False


def compact_preview(text: str) -> str:
    return re.sub(r"\s+", " ", text)[:180]


def main() -> None:
    args = parse_args()
    if args.top_k <= 0 or args.batch_size <= 0:
        raise SystemExit("--top-k and --batch-size must be positive integers.")

    chunks = load_jsonl(args.chunks)
    cases = load_jsonl(args.cases)
    gold_by_id = {}
    if args.gold_standard:
        gold_by_id = {record["id"]: record for record in load_jsonl(args.gold_standard)}
    if not chunks:
        raise SystemExit("No chunks found.")
    fingerprint = corpus_fingerprint(chunks)
    metadata_destination = args.embeddings_output.with_suffix(".metadata.json")

    print(f"Loading local model: {args.model}")
    model = SentenceTransformer(
        args.model,
        cache_folder=str(args.model_cache),
        device=args.device,
        local_files_only=True,
    )
    embeddings, reused = load_or_build_embeddings(
        model,
        chunks,
        args.embeddings_output,
        metadata_destination,
        args.batch_size,
        args.reuse_embeddings,
        fingerprint,
        args.model,
    )
    if embeddings.shape[0] != len(chunks):
        raise SystemExit("Embedding matrix row count does not match the chunk corpus.")
    print(
        f"{'Reused' if reused else 'Built'} {embeddings.shape[0]} embeddings "
        f"with {embeddings.shape[1]} dimensions."
    )

    query_embeddings = model.encode(
        [case["user_message"] for case in cases],
        batch_size=args.batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    results: list[dict] = []
    for case, query_embedding in zip(cases, query_embeddings, strict=True):
        allowed_stages = set(case["expected_stage_filters"])
        candidate_indices = [
            index for index, chunk in enumerate(chunks) if chunk["stage"] in allowed_stages
        ]
        if not candidate_indices:
            raise SystemExit(f"No candidate chunks for {case['id']} and its stage filters.")
        candidate_matrix = embeddings[candidate_indices]
        scores = candidate_matrix @ query_embedding
        ranked_positions = np.argsort(-scores)[: args.top_k]

        matching_hints: set[str] = set()
        gold = gold_by_id.get(case["id"], {})
        primary_paths = {item["path"] for item in gold.get("primary_evidence", [])}
        alternative_paths = {item["path"] for item in gold.get("acceptable_alternatives", [])}
        primary_hits: set[str] = set()
        alternative_hits: set[str] = set()
        top_results: list[dict] = []
        for rank, ranked_position in enumerate(ranked_positions, start=1):
            chunk_index = candidate_indices[int(ranked_position)]
            chunk = chunks[chunk_index]
            for hint in case["expected_path_hints"]:
                if hint_matches(chunk["source_path"], hint):
                    matching_hints.add(hint)
            if chunk["source_path"] in primary_paths:
                primary_hits.add(chunk["source_path"])
            if chunk["source_path"] in alternative_paths:
                alternative_hits.add(chunk["source_path"])
            top_results.append(
                {
                    "rank": rank,
                    "score": round(float(scores[ranked_position]), 4),
                    "chunk_id": chunk["chunk_id"],
                    "source_path": chunk["source_path"],
                    "title": chunk["title"],
                    "heading_path": chunk["heading_path"],
                    "preview": compact_preview(chunk["text"]),
                }
            )
        results.append(
            {
                "id": case["id"],
                "priority": case["priority"],
                "user_message": case["user_message"],
                "expected_stage_filters": case["expected_stage_filters"],
                "expected_path_hints": case["expected_path_hints"],
                "minimum_relevant_hits": case["minimum_relevant_hits"],
                "matched_path_hints": sorted(matching_hints),
                "passed": len(matching_hints) >= case["minimum_relevant_hits"],
                "gold_primary_hits": sorted(primary_hits),
                "gold_alternative_hits": sorted(alternative_hits),
                "gold_primary_recalled": bool(primary_hits),
                "gold_evidence_recalled": bool(primary_hits or alternative_hits),
                "top_results": top_results,
            }
        )

    passed = sum(result["passed"] for result in results)
    gold_primary_recalled = sum(result["gold_primary_recalled"] for result in results)
    gold_evidence_recalled = sum(result["gold_evidence_recalled"] for result in results)
    report = {
        "method": "dense cosine retrieval with local BAAI/bge-m3 embeddings",
        "model": args.model,
        "device": args.device,
        "top_k": args.top_k,
        "embedding_dimensions": int(embeddings.shape[1]),
        "embeddings_output": str(args.embeddings_output),
        "embeddings_metadata_output": str(metadata_destination),
        "corpus_fingerprint": fingerprint,
        "embeddings_reused": reused,
        "cases": len(results),
        "passed": passed,
        "pass_rate": round(passed / len(results), 4) if results else 0,
        "gold_primary_recalled": gold_primary_recalled,
        "gold_primary_recall_rate": round(gold_primary_recalled / len(results), 4) if results else 0,
        "gold_evidence_recalled": gold_evidence_recalled,
        "gold_evidence_recall_rate": round(gold_evidence_recalled / len(results), 4) if results else 0,
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                key: report[key]
                for key in (
                    "method",
                    "model",
                    "top_k",
                    "embedding_dimensions",
                    "cases",
                    "passed",
                    "pass_rate",
                    "gold_primary_recalled",
                    "gold_primary_recall_rate",
                    "gold_evidence_recalled",
                    "gold_evidence_recall_rate",
                )
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
