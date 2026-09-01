from __future__ import annotations

import argparse
import importlib.util
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "setup_codex_rag", PROJECT_ROOT / "tools" / "setup_codex_rag.py"
)
assert SPEC and SPEC.loader
setup_codex_rag = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(setup_codex_rag)


class SetupCodexRagTests(unittest.TestCase):
    def test_default_command_requires_license_acceptance(self) -> None:
        args = argparse.Namespace(
            default_aipm=True,
            accept_aipm_license=False,
        )
        with self.assertRaises(SystemExit):
            setup_codex_rag.knowledge_base_command(args, "python")

    def test_default_command_uses_current_python_and_license_flag(self) -> None:
        args = argparse.Namespace(
            default_aipm=True,
            accept_aipm_license=True,
            device="cpu",
            batch_size=8,
        )
        command = setup_codex_rag.knowledge_base_command(args, "C:/python.exe")
        self.assertEqual(command[:2], ["C:/python.exe", str(PROJECT_ROOT / "tools" / "setup_knowledge_base.py")])
        self.assertIn("--accept-aipm-license", command)

    def test_mcp_command_registers_the_project_server(self) -> None:
        command = setup_codex_rag.mcp_add_command("aipm_local_evidence", "C:/python.exe")
        self.assertEqual(command[:5], ["codex", "mcp", "add", "aipm_local_evidence", "--"])
        self.assertEqual(command[-1], str(PROJECT_ROOT / "mcp_server" / "aipm_retrieval_server.py"))


if __name__ == "__main__":
    unittest.main()
