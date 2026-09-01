#!/usr/bin/env python3
"""Expose the local AIPM Wiki retriever as a model-callable MCP tool.

Run this process over stdio. Codex starts it when a task needs the configured
tool; the embedding model is loaded lazily only on the first tool call.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from mcp.server.mcpserver import MCPServer  # noqa: E402
from rag.knowledge_base_config import load_active_knowledge_base  # noqa: E402
from rag.local_retriever import ALL_STAGES, LocalEvidenceRetriever  # noqa: E402


TOOL_NAME = "retrieve_aipm_evidence"
_retriever: LocalEvidenceRetriever | None = None


def _get_retriever() -> LocalEvidenceRetriever:
    global _retriever
    if _retriever is None:
        paths = load_active_knowledge_base(PROJECT_ROOT)
        _retriever = LocalEvidenceRetriever(
            chunks_path=paths.chunks_path,
            embeddings_path=paths.embeddings_path,
            model_cache=paths.model_cache,
            routing_config=paths.routing_config,
        )
    return _retriever


def validated_stages(stages: list[str] | None) -> tuple[str, ...]:
    """Accept an explicit subset or intentionally allow an all-corpus search."""
    if not stages:
        return ALL_STAGES
    normalized = tuple(dict.fromkeys(stage.strip().lower() for stage in stages if stage.strip()))
    invalid = sorted(set(normalized) - set(ALL_STAGES))
    if invalid:
        raise ValueError(f"Unknown stages: {', '.join(invalid)}. Allowed stages: {', '.join(ALL_STAGES)}.")
    return normalized or ALL_STAGES


mcp = MCPServer(
    name="aipm-local-evidence",
    title="AIPM Wiki Local Evidence",
    version="1.0.0",
    instructions=(
        "Use this tool for evidence from the local AIPM Wiki. It supplies background information, "
        "not facts about a user's experience. If personal evidence is missing, ask the user rather than infer it."
    ),
)


@mcp.tool(
    name=TOOL_NAME,
    title="Retrieve AIPM Wiki evidence",
    description=(
        "Search the local AIPM Wiki for evidence about AI product career direction, learning topics, "
        "RAG, tool calling, Agents, evaluation, cases, interviews, and resources. Call this when the "
        "user asks for factual guidance, career transition framing, a learning plan, or a source-backed "
        "answer. Do not call it merely to rewrite text unrelated to AI product work. Use stage filters when "
        "the request is clear; omit stages if a cross-library search is genuinely useful. Returned evidence "
        "must be cited by title and source_url in the final answer."
    ),
    structured_output=True,
)
def retrieve_aipm_evidence(
    query: str,
    stages: list[str] | None = None,
    max_results: int = 5,
) -> dict[str, Any]:
    """Return cited local evidence; the tool never performs web search or changes local data."""
    cleaned_query = query.strip()
    if not cleaned_query:
        raise ValueError("query must not be empty.")
    if not 1 <= max_results <= 8:
        raise ValueError("max_results must be between 1 and 8.")
    selected_stages = validated_stages(stages)
    return _get_retriever().retrieve(cleaned_query, stages=selected_stages, final_top_k=max_results)


if __name__ == "__main__":
    mcp.run(transport="stdio")
