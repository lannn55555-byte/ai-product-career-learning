#!/usr/bin/env python3
"""Evaluate a local hybrid retriever: BM25-style lexical + BGE-M3 dense search.

The script retrieves broad candidate pools independently, combines their rankings
with Reciprocal Rank Fusion (RRF), and applies a small, explainable penalty to
navigation-only README pages. It deliberately does not use a reranker yet: this
report is the evidence for deciding whether that added model is necessary.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from run_keyword_retrieval_baseline import B, K1, hint_matches, tokenize


DEFAULT_MODEL = "BAAI/bge-m3"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunks", required=True, type=Path)
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--gold-standard", type=Path)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--model-cache", required=True, type=Path)
    parser.add_argument("--embeddings", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--keyword-top-k", type=int, default=20)
    parser.add_argument("--dense-top-k", type=int, default=20)
    parser.add_argument("--final-top-k", type=int, default=5)
    parser.add_argument("--rrf-k", type=int, default=60)
    parser.add_argument("--lexical-weight", type=float, default=1.0)
    parser.add_argument("--dense-weight", type=float, default=1.0)
    parser.add_argument("--navigation-penalty", type=float, default=0.003)
    parser.add_argument(
        "--max-chunks-per-document",
        type=int,
        default=2,
        help="Maximum final evidence chunks from one source document; set 0 to disable.",
    )
    parser.add_argument(
        "--routing-config",
        type=Path,
        help="Optional intent-routing JSON. Its boosts reorder candidates but never bypass stage filters.",
    )
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--device", default="cpu")
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def is_navigation_page(chunk: dict) -> bool:
    return Path(chunk["source_path"]).name.lower() == "readme.md"


def compact_preview(text: str) -> str:
    return re.sub(r"\s+", " ", text)[:180]


def load_routes(path: Path | None) -> list[dict]:
    if path is None:
        return []
    with path.open(encoding="utf-8") as handle:
        config = json.load(handle)
    return config.get("routes", [])


def route_for_query(query: str, routes: list[dict]) -> dict | None:
    normalized = query.lower()
    for route in routes:
        if any(re.search(pattern, normalized, flags=re.IGNORECASE) for pattern in route["regex_patterns"]):
            return route
    return None


def route_boost(chunk: dict, route: dict | None) -> float:
    if route is None:
        return 0.0
    boost = float(route.get("stage_boosts", {}).get(chunk["stage"], 0.0))
    for prefix, value in route.get("path_prefix_boosts", {}).items():
        if chunk["source_path"].startswith(prefix):
            boost += float(value)
    return boost


def retrieval_query(query: str, route: dict | None) -> str:
    """Add a transparent intent-specific retrieval phrase, never a source path."""
    if route is None or not route.get("query_expansion"):
        return query
    return f"{query}\n检索主题：{route['query_expansion']}"


def build_bm25_index(chunks: list[dict]) -> tuple[list[Counter[str]], Counter[str], list[int], float]:
    token_counts: list[Counter[str]] = []
    document_frequency: Counter[str] = Counter()
    lengths: list[int] = []
    for chunk in chunks:
        counts = Counter(tokenize(chunk["retrieval_text"]))
        token_counts.append(counts)
        lengths.append(sum(counts.values()))
        document_frequency.update(counts.keys())
    return token_counts, document_frequency, lengths, sum(lengths) / len(lengths)


def lexical_ranking(
    query: str,
    candidate_indices: list[int],
    token_counts: list[Counter[str]],
    document_frequency: Counter[str],
    lengths: list[int],
    average_length: float,
    corpus_size: int,
    top_k: int,
) -> list[tuple[float, int]]:
    query_counts = Counter(tokenize(query))
    scores: list[tuple[float, int]] = []
    for index in candidate_indices:
        score = 0.0
        for term, query_frequency in query_counts.items():
            term_frequency = token_counts[index].get(term, 0)
            if not term_frequency:
                continue
            inverse_frequency = math.log(
                1 + (corpus_size - document_frequency[term] + 0.5) / (document_frequency[term] + 0.5)
            )
            normalized_frequency = term_frequency * (K1 + 1) / (
                term_frequency + K1 * (1 - B + B * lengths[index] / average_length)
            )
            score += query_frequency * inverse_frequency * normalized_frequency
        if score:
            scores.append((score, index))
    return sorted(scores, key=lambda pair: pair[0], reverse=True)[:top_k]


def select_final_evidence(
    ranked: list[tuple[float, float, int]], chunks: list[dict], final_top_k: int, max_per_document: int
) -> list[tuple[float, float, int]]:
    """Diversify final evidence without limiting the broad retrieval candidate pool.

    A document can contribute two final chunks. When it does, an adjacent chunk is
    selected before a distant chunk, preserving a continuous argument where possible.
    Non-adjacent second chunks remain fallback candidates if diversification cannot
    fill the requested final Top-K.
    """
    if max_per_document == 0:
        return ranked[:final_top_k]

    selected: list[tuple[float, float, int]] = []
    deferred: list[tuple[float, float, int]] = []
    selected_positions: dict[str, list[int]] = {}
    for item in ranked:
        _, _, index = item
        chunk = chunks[index]
        document_id = chunk["document_id"]
        positions = selected_positions.setdefault(document_id, [])
        if len(positions) >= max_per_document:
            continue
        if positions and len(positions) == 1:
            if abs(chunk["document_chunk_position"] - positions[0]) > 1:
                deferred.append(item)
                continue
        selected.append(item)
        positions.append(chunk["document_chunk_position"])
        if len(selected) == final_top_k:
            return selected

    for item in deferred:
        _, _, index = item
        document_id = chunks[index]["document_id"]
        positions = selected_positions.setdefault(document_id, [])
        if len(positions) >= max_per_document:
            continue
        selected.append(item)
        positions.append(chunks[index]["document_chunk_position"])
        if len(selected) == final_top_k:
            break
    return selected


def main() -> None:
    args = parse_args()
    if min(args.keyword_top_k, args.dense_top_k, args.final_top_k, args.rrf_k, args.batch_size) <= 0:
        raise SystemExit("Top-K, RRF-K, and batch size must be positive.")
    if args.max_chunks_per_document < 0:
        raise SystemExit("--max-chunks-per-document cannot be negative.")
    if args.navigation_penalty < 0 or args.lexical_weight < 0 or args.dense_weight < 0:
        raise SystemExit("Weights and navigation penalty cannot be negative.")
    if args.lexical_weight == 0 and args.dense_weight == 0:
        raise SystemExit("At least one retrieval weight must be greater than zero.")

    chunks = load_jsonl(args.chunks)
    cases = load_jsonl(args.cases)
    gold_by_id = {}
    if args.gold_standard:
        gold_by_id = {record["id"]: record for record in load_jsonl(args.gold_standard)}
    routes = load_routes(args.routing_config)
    embeddings = np.load(args.embeddings)
    if embeddings.shape[0] != len(chunks):
        raise SystemExit("Embedding matrix row count does not match the chunk corpus.")

    token_counts, document_frequency, lengths, average_length = build_bm25_index(chunks)
    print(f"Loading local model: {args.model}")
    model = SentenceTransformer(
        args.model,
        cache_folder=str(args.model_cache),
        device=args.device,
        local_files_only=True,
    )
    routed_queries = [
        retrieval_query(case["user_message"], route_for_query(case["user_message"], routes))
        for case in cases
    ]
    query_embeddings = model.encode(
        routed_queries,
        batch_size=args.batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    results: list[dict] = []
    for case, query_embedding, query_for_retrieval in zip(cases, query_embeddings, routed_queries, strict=True):
        route = route_for_query(case["user_message"], routes)
        allowed_stages = set(case["expected_stage_filters"])
        candidate_indices = [
            index for index, chunk in enumerate(chunks) if chunk["stage"] in allowed_stages
        ]
        lexical = lexical_ranking(
            query_for_retrieval,
            candidate_indices,
            token_counts,
            document_frequency,
            lengths,
            average_length,
            len(chunks),
            args.keyword_top_k,
        )
        dense_scores = embeddings[candidate_indices] @ query_embedding
        dense_positions = np.argsort(-dense_scores)[: args.dense_top_k]
        dense = [(float(dense_scores[position]), candidate_indices[int(position)]) for position in dense_positions]

        fused: dict[int, dict] = {}
        for rank, (score, index) in enumerate(lexical, start=1):
            fused.setdefault(index, {"lexical_rank": None, "dense_rank": None, "lexical_score": None, "dense_score": None})
            fused[index].update({"lexical_rank": rank, "lexical_score": score})
        for rank, (score, index) in enumerate(dense, start=1):
            fused.setdefault(index, {"lexical_rank": None, "dense_rank": None, "lexical_score": None, "dense_score": None})
            fused[index].update({"dense_rank": rank, "dense_score": score})

        ranked: list[tuple[float, float, int]] = []
        for index, record in fused.items():
            rrf_score = 0.0
            if record["lexical_rank"] is not None:
                rrf_score += args.lexical_weight / (args.rrf_k + record["lexical_rank"])
            if record["dense_rank"] is not None:
                rrf_score += args.dense_weight / (args.rrf_k + record["dense_rank"])
            penalty = args.navigation_penalty if is_navigation_page(chunks[index]) else 0.0
            intent_boost = route_boost(chunks[index], route)
            record["rrf_score"] = rrf_score
            record["navigation_penalty"] = penalty
            record["intent_boost"] = intent_boost
            ranked.append((rrf_score - penalty + intent_boost, rrf_score, index))
        ranked.sort(key=lambda item: item[0], reverse=True)

        matching_hints: set[str] = set()
        gold = gold_by_id.get(case["id"], {})
        primary_paths = {item["path"] for item in gold.get("primary_evidence", [])}
        alternative_paths = {item["path"] for item in gold.get("acceptable_alternatives", [])}
        primary_hits: set[str] = set()
        alternative_hits: set[str] = set()
        top_results: list[dict] = []
        final_evidence = select_final_evidence(
            ranked, chunks, args.final_top_k, args.max_chunks_per_document
        )
        for rank, (final_score, rrf_score, index) in enumerate(final_evidence, start=1):
            chunk = chunks[index]
            for hint in case["expected_path_hints"]:
                if hint_matches(chunk["source_path"], hint):
                    matching_hints.add(hint)
            if chunk["source_path"] in primary_paths:
                primary_hits.add(chunk["source_path"])
            if chunk["source_path"] in alternative_paths:
                alternative_hits.add(chunk["source_path"])
            record = fused[index]
            top_results.append(
                {
                    "rank": rank,
                    "score": round(final_score, 6),
                    "rrf_score": round(rrf_score, 6),
                    "navigation_penalty": record["navigation_penalty"],
                    "intent_boost": record["intent_boost"],
                    "lexical_rank": record["lexical_rank"],
                    "dense_rank": record["dense_rank"],
                    "lexical_score": round(record["lexical_score"], 4) if record["lexical_score"] is not None else None,
                    "dense_score": round(record["dense_score"], 4) if record["dense_score"] is not None else None,
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
                "retrieval_query": query_for_retrieval,
                "expected_stage_filters": case["expected_stage_filters"],
                "expected_path_hints": case["expected_path_hints"],
                "minimum_relevant_hits": case["minimum_relevant_hits"],
                "matched_path_hints": sorted(matching_hints),
                "passed": len(matching_hints) >= case["minimum_relevant_hits"],
                "gold_primary_hits": sorted(primary_hits),
                "gold_alternative_hits": sorted(alternative_hits),
                "gold_primary_recalled": bool(primary_hits),
                "gold_evidence_recalled": bool(primary_hits or alternative_hits),
                "intent_route": route["name"] if route else None,
                "candidate_pool_size": len(fused),
                "top_results": top_results,
            }
        )

    passed = sum(result["passed"] for result in results)
    primary_recalled = sum(result["gold_primary_recalled"] for result in results)
    evidence_recalled = sum(result["gold_evidence_recalled"] for result in results)
    report = {
        "method": "hybrid lexical + dense retrieval with Reciprocal Rank Fusion and README navigation penalty",
        "model": args.model,
        "keyword_top_k": args.keyword_top_k,
        "dense_top_k": args.dense_top_k,
        "final_top_k": args.final_top_k,
        "rrf_k": args.rrf_k,
        "lexical_weight": args.lexical_weight,
        "dense_weight": args.dense_weight,
        "navigation_penalty": args.navigation_penalty,
        "max_chunks_per_document": args.max_chunks_per_document,
        "routing_config": str(args.routing_config) if args.routing_config else None,
        "cases": len(results),
        "passed": passed,
        "pass_rate": round(passed / len(results), 4) if results else 0,
        "gold_primary_recalled": primary_recalled,
        "gold_primary_recall_rate": round(primary_recalled / len(results), 4) if results else 0,
        "gold_evidence_recalled": evidence_recalled,
        "gold_evidence_recall_rate": round(evidence_recalled / len(results), 4) if results else 0,
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in report if key != "results"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
