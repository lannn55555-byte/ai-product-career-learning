"""Static checks for the checked-in cross-host workflow adapters."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class HostAdapterTests(unittest.TestCase):
    def test_claude_code_has_project_mcp_and_router_skill(self) -> None:
        config = json.loads((PROJECT_ROOT / ".mcp.json").read_text(encoding="utf-8"))
        server = config["mcpServers"]["aipm_local_evidence"]
        self.assertEqual(server["type"], "stdio")
        self.assertIn("CLAUDE_PROJECT_DIR", server["args"][0])
        router = (PROJECT_ROOT / ".claude" / "skills" / "ai-product-career-learning" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Read `AGENTS.md`", router)
        self.assertIn("retrieve_aipm_evidence", router)

    def test_cursor_has_workspace_mcp_and_always_on_rule(self) -> None:
        config = json.loads((PROJECT_ROOT / ".cursor" / "mcp.json").read_text(encoding="utf-8"))
        server = config["mcpServers"]["aipm_local_evidence"]
        self.assertEqual(server["type"], "stdio")
        self.assertIn("${workspaceFolder}", server["args"][0])
        rule = (PROJECT_ROOT / ".cursor" / "rules" / "ai-product-career-learning.mdc").read_text(encoding="utf-8")
        self.assertIn("alwaysApply: true", rule)
        self.assertIn("AGENTS.md", rule)

    def test_antigravity_has_workspace_mcp_and_rule(self) -> None:
        config = json.loads((PROJECT_ROOT / ".agents" / "mcp_config.json").read_text(encoding="utf-8"))
        server = config["mcpServers"]["aipm_local_evidence"]
        self.assertEqual(server["command"], "python")
        self.assertEqual(server["cwd"], ".")
        rule = (PROJECT_ROOT / ".agents" / "rules" / "ai-product-career-learning.md").read_text(encoding="utf-8")
        self.assertIn("AGENTS.md", rule)

    def test_cross_host_guide_does_not_overclaim(self) -> None:
        guide = (PROJECT_ROOT / "integrations" / "README.md").read_text(encoding="utf-8")
        self.assertIn("does not merge", guide)
        self.assertIn("not identical UI", guide)
        self.assertIn("Claude Desktop's local MCP", guide)

    def test_policy_uses_host_specific_setup(self) -> None:
        policy = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("In Codex, initialize the source", policy)
        self.assertIn("In Claude Code, Cursor, or Antigravity", policy)
        self.assertIn("only for first-time Codex setup", policy)


if __name__ == "__main__":
    unittest.main()
