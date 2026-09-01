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
        self.assertIn("Treat this as an onboarding decision", policy)
        self.assertIn("Do not wait for the user to mention RAG", policy)
        self.assertIn("third-party material and a local embedding model", policy)
        self.assertIn("explicit user confirmation", policy)

    def test_core_entry_skills_do_not_require_user_to_name_rag(self) -> None:
        for name in CORE_SKILLS:
            skill = (PROJECT_ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("First-use evidence onboarding", skill, name)
            self.assertIn("proactively offer", skill, name)
            self.assertIn("do not invent a setup command", " ".join(skill.lower().split()), name)


if __name__ == "__main__":
    unittest.main()
