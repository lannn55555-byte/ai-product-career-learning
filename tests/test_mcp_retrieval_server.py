"""Offline tests for the local MCP retrieval tool's input boundary."""

from __future__ import annotations

import unittest

from mcp_server.aipm_retrieval_server import ALL_STAGES, validated_stages


class McpRetrievalServerTests(unittest.TestCase):
    def test_empty_stage_selection_intentionally_searches_all_stages(self) -> None:
        self.assertEqual(validated_stages(None), ALL_STAGES)

    def test_stage_selection_is_deduplicated(self) -> None:
        self.assertEqual(validated_stages(["diagnosis", "learning", "diagnosis"]), ("diagnosis", "learning"))

    def test_unknown_stage_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validated_stages(["anything"])


if __name__ == "__main__":
    unittest.main()
