"""Resolve the local knowledge base selected for the MCP retriever."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


class KnowledgeBaseSetupRequired(RuntimeError):
    """Raised when no usable local corpus has been initialized."""


@dataclass(frozen=True)
class KnowledgeBasePaths:
    name: str
    chunks_path: Path
    embeddings_path: Path
    model_cache: Path
    routing_config: Path | None


def active_config_path(project_root: Path) -> Path:
    return project_root / "rag" / "local" / "active_knowledge_base.json"


def _resolve(project_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else project_root / path


def load_active_knowledge_base(project_root: Path) -> KnowledgeBasePaths:
    config_path = active_config_path(project_root)
    if not config_path.is_file():
        legacy = KnowledgeBasePaths(
            name="Legacy AIPM Wiki local knowledge base",
            chunks_path=project_root / "rag" / "generated" / "aipm-wiki" / "chunks.jsonl",
            embeddings_path=project_root / "rag" / "generated" / "bge-m3" / "chunk_embeddings.npy",
            model_cache=project_root / "rag" / "models" / "bge-m3",
            routing_config=project_root / "rag" / "config" / "intent_routes_v1.json",
        )
        if legacy.chunks_path.is_file() and legacy.embeddings_path.is_file():
            return legacy
        raise KnowledgeBaseSetupRequired(
            "No local knowledge base is initialized. Run tools/setup_knowledge_base.py first."
        )
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
        paths = KnowledgeBasePaths(
            name=str(data["name"]),
            chunks_path=_resolve(project_root, str(data["chunks_path"])),
            embeddings_path=_resolve(project_root, str(data["embeddings_path"])),
            model_cache=_resolve(project_root, str(data["model_cache"])),
            routing_config=(
                _resolve(project_root, str(data["routing_config"]))
                if data.get("routing_config")
                else None
            ),
        )
    except (KeyError, json.JSONDecodeError) as error:
        raise KnowledgeBaseSetupRequired(f"Invalid knowledge-base config: {config_path}") from error
    missing = [path for path in (paths.chunks_path, paths.embeddings_path) if not path.is_file()]
    if missing:
        raise KnowledgeBaseSetupRequired(
            "The selected local knowledge base is incomplete. Run tools/setup_knowledge_base.py again."
        )
    return paths
