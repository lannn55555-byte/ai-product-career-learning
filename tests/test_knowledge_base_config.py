from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from rag.knowledge_base_config import KnowledgeBaseSetupRequired, load_active_knowledge_base


class KnowledgeBaseConfigTests(unittest.TestCase):
    def test_missing_config_requires_setup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(KnowledgeBaseSetupRequired):
                load_active_knowledge_base(Path(directory))

    def test_relative_paths_resolve_from_project_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            chunks = root / "rag/generated/test/chunks.jsonl"
            embeddings = root / "rag/generated/test/chunk_embeddings.npy"
            chunks.parent.mkdir(parents=True)
            chunks.write_text("", encoding="utf-8")
            embeddings.write_bytes(b"test")
            config = root / "rag/local/active_knowledge_base.json"
            config.parent.mkdir(parents=True)
            config.write_text(json.dumps({
                "name": "Test source",
                "chunks_path": "rag/generated/test/chunks.jsonl",
                "embeddings_path": "rag/generated/test/chunk_embeddings.npy",
                "model_cache": "rag/models/bge-m3",
                "routing_config": None,
            }), encoding="utf-8")
            selected = load_active_knowledge_base(root)
            self.assertEqual(selected.name, "Test source")
            self.assertEqual(selected.chunks_path, chunks)

    def test_legacy_aipm_paths_remain_usable_without_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            chunks = root / "rag/generated/aipm-wiki/chunks.jsonl"
            embeddings = root / "rag/generated/bge-m3/chunk_embeddings.npy"
            chunks.parent.mkdir(parents=True)
            embeddings.parent.mkdir(parents=True)
            chunks.write_text("", encoding="utf-8")
            embeddings.write_bytes(b"test")
            selected = load_active_knowledge_base(root)
            self.assertEqual(selected.chunks_path, chunks)


if __name__ == "__main__":
    unittest.main()
