"""Local, evidence-first hybrid retriever for the AI Product Growth Agent.

This module is deliberately framework-neutral. A CLI, MCP server, or HTTP API can
create one LocalEvidenceRetriever at startup and call retrieve() for each request.
The corpus, embedding matrix, BM25 index, and embedding model stay in memory while
the host process remains alive.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


ALL_STAGES = ("diagnosis", "learning", "application", "case", "interview", "resources")
DEFAULT_MODEL = "BAAI/bge-m3"
K1 = 1.2
B = 0.75
DYNAMIC_QUERY = re.compile(r"最新|现在|目前|今日|价格|报价|招聘|在招|jd|发布|上线|截至", re.IGNORECASE)


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


def load_routes(path: Path | None) -> list[dict]:
    if path is None:
        return []
    with path.open(encoding="utf-8") as handle:
        return json.load(handle).get("routes", [])


def route_for_query(query: str, routes: list[dict]) -> dict | None:
    normalized = query.lower()
    for route in routes:
        if any(re.search(pattern, normalized, flags=re.IGNORECASE) for pattern in route["regex_patterns"]):
            return route
    return None


def retrieval_query(query: str, route: dict | None) -> str:
    if route is None or not route.get("query_expansion"):
        return query
    return f"{query}\n检索主题：{route['query_expansion']}"


def route_boost(chunk: dict, route: dict | None) -> float:
    if route is None:
        return 0.0
    boost = float(route.get("stage_boosts", {}).get(chunk["stage"], 0.0))
    for prefix, value in route.get("path_prefix_boosts", {}).items():
        if chunk["source_path"].startswith(prefix):
            boost += float(value)
    return boost


def is_navigation_page(chunk: dict) -> bool:
    return Path(chunk["source_path"]).name.lower() == "readme.md"


class LocalEvidenceRetriever:
    def __init__(
        self,
        chunks_path: Path,
        embeddings_path: Path,
        model_cache: Path,
        routing_config: Path | None = None,
        model_name: str = DEFAULT_MODEL,
        device: str = "cpu",
    ) -> None:
        self.chunks = load_jsonl(chunks_path)
        self.embeddings = np.load(embeddings_path)
        if self.embeddings.shape[0] != len(self.chunks):
            raise ValueError("Embedding matrix row count does not match the chunk corpus.")
        self.routes = load_routes(routing_config)
        self.token_counts: list[Counter[str]] = []
        self.document_frequency: Counter[str] = Counter()
        self.lengths: list[int] = []
        for chunk in self.chunks:
            counts = Counter(tokenize(chunk["retrieval_text"]))
            self.token_counts.append(counts)
            self.document_frequency.update(counts.keys())
            self.lengths.append(sum(counts.values()))
        self.average_length = sum(self.lengths) / len(self.lengths)
        self.model_name = model_name
        self.model = SentenceTransformer(
            model_name,
            cache_folder=str(model_cache),
            device=device,
            local_files_only=True,
        )

    def _lexical_ranking(self, query: str, candidate_indices: list[int], top_k: int) -> list[tuple[float, int]]:
        query_counts = Counter(tokenize(query))
        scores: list[tuple[float, int]] = []
        for index in candidate_indices:
            score = 0.0
            for term, query_frequency in query_counts.items():
                term_frequency = self.token_counts[index].get(term, 0)
                if not term_frequency:
                    continue
                inverse_frequency = math.log(
                    1
                    + (len(self.chunks) - self.document_frequency[term] + 0.5)
                    / (self.document_frequency[term] + 0.5)
                )
                normalized_frequency = term_frequency * (K1 + 1) / (
                    term_frequency + K1 * (1 - B + B * self.lengths[index] / self.average_length)
                )
                score += query_frequency * inverse_frequency * normalized_frequency
            if score:
                scores.append((score, index))
        return sorted(scores, key=lambda pair: pair[0], reverse=True)[:top_k]

    @staticmethod
    def _select_final(
        ranked: list[tuple[float, float, int]], chunks: list[dict], top_k: int, max_per_document: int
    ) -> list[tuple[float, float, int]]:
        if max_per_document == 0:
            return ranked[:top_k]
        selected: list[tuple[float, float, int]] = []
        deferred: list[tuple[float, float, int]] = []
        positions: dict[str, list[int]] = {}
        for item in ranked:
            _, _, index = item
            chunk = chunks[index]
            doc_positions = positions.setdefault(chunk["document_id"], [])
            if len(doc_positions) >= max_per_document:
                continue
            if len(doc_positions) == 1 and abs(chunk["document_chunk_position"] - doc_positions[0]) > 1:
                deferred.append(item)
                continue
            selected.append(item)
            doc_positions.append(chunk["document_chunk_position"])
            if len(selected) == top_k:
                return selected
        for item in deferred:
            _, _, index = item
            doc_positions = positions.setdefault(chunks[index]["document_id"], [])
            if len(doc_positions) < max_per_document:
                selected.append(item)
                doc_positions.append(chunks[index]["document_chunk_position"])
            if len(selected) == top_k:
                break
        return selected

    def retrieve(
        self,
        query: str,
        stages: tuple[str, ...] = ALL_STAGES,
        final_top_k: int = 5,
        keyword_top_k: int = 20,
        dense_top_k: int = 20,
        lexical_weight: float = 1.0,
        dense_weight: float = 1.0,
        rrf_k: int = 60,
        navigation_penalty: float = 0.003,
        max_chunks_per_document: int = 2,
    ) -> dict:
        if not query.strip():
            raise ValueError("query cannot be empty")
        stage_filter = tuple(dict.fromkeys(stages))
        unknown_stages = set(stage_filter) - set(ALL_STAGES)
        if unknown_stages:
            raise ValueError(f"Unknown stages: {sorted(unknown_stages)}")
        if not stage_filter:
            raise ValueError("At least one stage is required")
        route = route_for_query(query, self.routes)
        query_for_retrieval = retrieval_query(query, route)
        candidate_indices = [
            index for index, chunk in enumerate(self.chunks) if chunk["stage"] in set(stage_filter)
        ]
        lexical = self._lexical_ranking(query_for_retrieval, candidate_indices, keyword_top_k)
        query_embedding = self.model.encode(
            [query_for_retrieval], convert_to_numpy=True, normalize_embeddings=True
        )[0]
        dense_scores = self.embeddings[candidate_indices] @ query_embedding
        dense_positions = np.argsort(-dense_scores)[:dense_top_k]
        dense = [(float(dense_scores[position]), candidate_indices[int(position)]) for position in dense_positions]

        fused: dict[int, dict] = {}
        for rank, (score, index) in enumerate(lexical, start=1):
            fused.setdefault(index, {"lexical_rank": None, "dense_rank": None})
            fused[index].update({"lexical_rank": rank, "lexical_score": score})
        for rank, (score, index) in enumerate(dense, start=1):
            fused.setdefault(index, {"lexical_rank": None, "dense_rank": None})
            fused[index].update({"dense_rank": rank, "dense_score": score})

        ranked: list[tuple[float, float, int]] = []
        for index, record in fused.items():
            rrf_score = 0.0
            if record["lexical_rank"] is not None:
                rrf_score += lexical_weight / (rrf_k + record["lexical_rank"])
            if record["dense_rank"] is not None:
                rrf_score += dense_weight / (rrf_k + record["dense_rank"])
            penalty = navigation_penalty if is_navigation_page(self.chunks[index]) else 0.0
            intent_boost = route_boost(self.chunks[index], route)
            record.update({"rrf_score": rrf_score, "navigation_penalty": penalty, "intent_boost": intent_boost})
            ranked.append((rrf_score - penalty + intent_boost, rrf_score, index))
        ranked.sort(key=lambda item: item[0], reverse=True)
        selected = self._select_final(ranked, self.chunks, final_top_k, max_chunks_per_document)

        evidence = []
        for rank, (score, rrf_score, index) in enumerate(selected, start=1):
            chunk = self.chunks[index]
            record = fused[index]
            evidence.append(
                {
                    "rank": rank,
                    "text": chunk["text"],
                    "title": chunk["title"],
                    "heading_path": chunk["heading_path"],
                    "source_path": chunk["source_path"],
                    "source_url": chunk["source_url"],
                    "stage": chunk["stage"],
                    "content_type": chunk["content_type"],
                    "freshness": chunk["freshness"],
                    "outbound_references": chunk["outbound_references"],
                    "retrieval_explanation": {
                        "lexical_rank": record["lexical_rank"],
                        "dense_rank": record["dense_rank"],
                        "intent_boost": record["intent_boost"],
                        "navigation_penalty": record["navigation_penalty"],
                        "final_score": round(score, 6),
                        "rrf_score": round(rrf_score, 6),
                    },
                }
            )
        return {
            "query": query,
            "retrieval_query": query_for_retrieval,
            "intent_route": route["name"] if route else None,
            "stage_filters": list(stage_filter),
            "web_verification_required": bool(DYNAMIC_QUERY.search(query)),
            "evidence": evidence,
            "usage_boundary": (
                "Use these as cited background evidence. If web_verification_required is true, "
                "verify dynamic claims with current official web sources before answering."
            ),
        }
