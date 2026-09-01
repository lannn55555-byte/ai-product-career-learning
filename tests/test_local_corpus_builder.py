from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class LocalCorpusBuilderTests(unittest.TestCase):
    def test_markdown_and_text_build_standard_chunks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            output = root / "output"
            source.mkdir()
            source.joinpath("rag.md").write_text("# RAG\\n\\n" + "知识检索与回答边界。 " * 30, encoding="utf-8")
            source.joinpath("notes.txt").write_text("Agent 的工具边界。 " * 30, encoding="utf-8")
            subprocess.run([
                sys.executable, str(PROJECT_ROOT / "tools" / "build_local_corpus.py"),
                "--source-root", str(source), "--output-root", str(output),
                "--source-name", "Test notes", "--source-id", "test-notes",
            ], cwd=PROJECT_ROOT, check=True, capture_output=True, text=True)
            chunks = [json.loads(line) for line in output.joinpath("chunks.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(chunks), 2)
            self.assertEqual({chunk["stage"] for chunk in chunks}, {"learning"})
            self.assertTrue(all(chunk["source_class"] == "learner_provided" for chunk in chunks))


if __name__ == "__main__":
    unittest.main()
