#!/usr/bin/env python3
"""Run a deterministic BM25-style keyword baseline against the local RAG chunks.

This deliberately has no external dependencies. It gives the project an auditable
lexical baseline before semantic embeddings or a vector database are introduced.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path


TOP_K = 5
K1 = 1.2
B = 0.75


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunks", required=True, type=Path)
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--gold-standard", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def chinese_bigrams(text: str) -> list[str]:
    terms: list[str] = []
    for run in re.findall(r"[\u4e00-\u9fff]+", text):
        if len(run) == 1:
            terms.append(run)
        else:
            terms.extend(run[index : index + 2] for index in range(len(run) - 1))
    return terms


def tokenize(text: str) -> list[str]:
    english_or_number = re.findall(r"[a-zA-Z][a-zA-Z0-9+.#_-]*|\d+(?:\.\d+)?", text.lower())
    return chinese_bigrams(text) + english_or_number


def hint_matches(path: str, hint: str) -> bool:
    return path.startswith(hint) if hint.endswith("/") else path == hint


def main() -> None:
    args = parse_args()
    chunks = load_jsonl(args.chunks)
    cases = load_jsonl(args.cases)
    gold_by_id = {}
    if args.gold_standard:
        gold_by_id = {record["id"]: record for record in load_jsonl(args.gold_standard)}
    args.output.parent.mkdir(parents=True, exist_ok=True)

    token_counts: list[Counter[str]] = []
    doc_frequency: Counter[str] = Counter()
    lengths: list[int] = []
    for chunk in chunks:
        counts = Counter(tokenize(chunk["retrieval_text"]))
        token_counts.append(counts)
        lengths.append(sum(counts.values()))
        doc_frequency.update(counts.keys())

    average_length = sum(lengths) / len(lengths)
    document_total = len(chunks)
    results: list[dict] = []

    for case in cases:
        allowed_stages = set(case["expected_stage_filters"])
        query_counts = Counter(tokenize(case["user_message"]))
        candidates: list[tuple[float, int]] = []
        for index, chunk in enumerate(chunks):
            if chunk["stage"] not in allowed_stages:
                continue
            score = 0.0
            document_length = lengths[index]
            for term, query_frequency in query_counts.items():
                term_frequency = token_counts[index].get(term, 0)
                if not term_frequency:
                    continue
                inverse_frequency = math.log(
                    1 + (document_total - doc_frequency[term] + 0.5) / (doc_frequency[term] + 0.5)
                )
                normalized_frequency = term_frequency * (K1 + 1) / (
                    term_frequency + K1 * (1 - B + B * document_length / average_length)
                )
                score += query_frequency * inverse_frequency * normalized_frequency
            if score:
                candidates.append((score, index))

        candidates.sort(key=lambda pair: pair[0], reverse=True)
        top = candidates[:TOP_K]
        matching_hints: set[str] = set()
        gold = gold_by_id.get(case["id"], {})
        primary_paths = {item["path"] for item in gold.get("primary_evidence", [])}
        alternative_paths = {item["path"] for item in gold.get("acceptable_alternatives", [])}
        primary_hits: set[str] = set()
        alternative_hits: set[str] = set()
        top_results: list[dict] = []
        for rank, (score, index) in enumerate(top, start=1):
            chunk = chunks[index]
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
                    "score": round(score, 4),
                    "chunk_id": chunk["chunk_id"],
                    "source_path": chunk["source_path"],
                    "title": chunk["title"],
                    "heading_path": chunk["heading_path"],
                    "preview": re.sub(r"\s+", " ", chunk["text"])[:180],
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
        "method": "BM25-style lexical retrieval over Chinese character bigrams and English tokens",
        "top_k": TOP_K,
        "cases": len(results),
        "passed": passed,
        "pass_rate": round(passed / len(results), 4) if results else 0,
        "gold_primary_recalled": gold_primary_recalled,
        "gold_primary_recall_rate": round(gold_primary_recalled / len(results), 4) if results else 0,
        "gold_evidence_recalled": gold_evidence_recalled,
        "gold_evidence_recall_rate": round(gold_evidence_recalled / len(results), 4) if results else 0,
        "results": results,
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                key: report[key]
                for key in (
                    "method",
                    "top_k",
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
