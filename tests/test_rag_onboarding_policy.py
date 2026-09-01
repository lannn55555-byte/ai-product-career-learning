"""Regression checks for the no-technical-knowledge first-use journey."""

from __future__ import annotations

import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORE_SKILLS = (
    "ai-career-transition-planner",
    "ai-career-sprint-plan",
    "adaptive-ai-learning-coach",
)


class RagOnboardingPolicyTests(unittest.TestCase):
    def test_project_policy_requires_proactive_plain_language_onboarding(self) -> None:
        policy = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        normalized_policy = " ".join(policy.split())
        self.assertIn("Treat this as an onboarding decision", policy)
        self.assertIn("Do not wait for the user to mention RAG", normalized_policy)
        self.assertIn("third-party material and a local embedding model", policy)
        self.assertIn("explicit user confirmation", policy)
        self.assertIn("End that same response with one direct", policy)
        self.assertIn("library as optional or unavailable", policy)

    def test_core_entry_skills_do_not_require_user_to_name_rag(self) -> None:
        for name in CORE_SKILLS:
            skill = (PROJECT_ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            normalized_skill = " ".join(skill.lower().split())
            self.assertIn("First-use evidence onboarding", skill, name)
            self.assertIn("proactively offer", normalized_skill, name)
            self.assertIn("direct question asking whether to enable it", skill, name)
            self.assertIn("never merely", normalized_skill, name)
            self.assertIn("do not invent a setup command", normalized_skill, name)


if __name__ == "__main__":
    unittest.main()
