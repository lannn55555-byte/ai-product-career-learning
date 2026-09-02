---
name: ai-product-career-learning
description: Run the local AI-product career-learning workflow in this repository: career direction, learning route, adaptive lessons, state, and local evidence retrieval.
---

# AI Product Career Learning workflow

Use this Skill when the user asks for AI-product career direction, a learning
route, a daily lesson or review, case strategy, interview positioning, or
AI-product resume help in this repository.

1. Read `AGENTS.md` before responding. It is the canonical policy for source
   boundaries, first-use knowledge-base onboarding, custom-source setup, and
   durable learning state.
2. Route to the canonical project Skill that matches the request:
   - career diagnosis: `skills/ai-career-transition-planner/SKILL.md`
   - route planning: `skills/ai-career-sprint-plan/SKILL.md`
   - daily learning or review: `skills/adaptive-ai-learning-coach/SKILL.md`
   - case strategy: `skills/ai-career-case-strategy/SKILL.md`
   - interview positioning: `skills/ai-career-interview-positioning/SKILL.md`
3. Treat `state/learning_plan.md` and `state/learning_state.md` as private,
   durable learner state. Follow the canonical Skill before creating or
   updating them.
4. Use `retrieve_aipm_evidence` only according to `AGENTS.md`. If the tool is
   unavailable, follow its onboarding and permission rules; never pretend that
   retrieval has run.

This adapter does not duplicate the learning method. The canonical Skills and
policy files remain the source of truth so Codex and Claude Code behave from
the same rules.
