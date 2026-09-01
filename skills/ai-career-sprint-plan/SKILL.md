---
name: ai-career-sprint-plan
description: Plan a personalized 14-, 30-, or 60-day transition route for AI-product roles. Diagnose product and AI foundations separately, then choose an AI bridge, dual-foundation, or product-repair learning mode.
---

# AI Career Sprint Planner

## Purpose

Create a personalized learning route and initialize durable state. Do not teach
the lessons, force a build, or promise job readiness. Daily dialogue teaching
belongs to `adaptive-ai-learning-coach`.

## First-use evidence onboarding

When the workspace contains this learning-agent project and the learner starts
an AI-product route or asks how to use the project, if
`retrieve_aipm_evidence` is unavailable, proactively offer the included local
reference library. Do not require the learner to know or mention RAG. Explain
the download, local files, and Codex-tool impact in plain language, then end
the same response with a direct question asking whether to enable it. Never
merely describe the library as optional or unavailable before continuing the
intake. After the learner agrees, obtain explicit acceptance of the AIPM-Wiki
terms in `THIRD_PARTY_NOTICES.md`, then run the project setup flow and ask them
to start a new task. If they decline, create the route from their verified
handoff and the Skill rules, clearly without presenting external guidance as
cited evidence.

If this project is not present in the workspace, do not invent a setup command
or imply that a knowledge base is enabled.

Support 14, 30, and 60 learning days. A 14-day route establishes a usable
framework and evidence of basic judgement; it is not a complete curriculum for
both product management and AI engineering.

Before planning, read:

- the verified Learning Handoff when available, otherwise the accepted
  diagnosis and relevant learner information;
- `../adaptive-ai-learning-coach/references/ai-product-learning-architecture.md`;
- `../adaptive-ai-learning-coach/references/learning-evidence-and-source-policy.md`;
- `../adaptive-ai-learning-coach/references/track-bridges.md` when pairing
  tracks; and
- `../adaptive-ai-learning-coach/references/model-landscape-and-selection.md`
  when model selection is included.

## Intake and foundation diagnosis

Use available evidence before asking questions. Ask only when a missing answer
changes the route:

1. deadline or route length: 14, 30, or 60 days;
2. target role or target JD, when known;
3. product-foundation evidence: problem framing, user research, requirement
   scope, flows, metrics, experiments, or delivery decisions;
4. AI-foundation evidence: model boundary, context, retrieval, tools, state,
   safety, or evaluation decisions; and
5. learning preferences or accessibility needs.

Do not infer product competence from a title or AI competence from using an AI
tool. Classify each foundation as **emerging**, **working**, or **unassessed**.
If unassessed, begin provisionally in dual-foundation mode and recalibrate after
the first two learning units.

## Select a learning mode

| Mode | Foundation profile | What the learner receives |
|---|---|---|
| **AI bridge** | Product working; AI emerging. | AI-mainline route with a concise product bridge each day. |
| **Dual foundation** | Product emerging, AI emerging, or both unassessed. | Two visible daily blocks: product foundation and AI mainline, connected through one product decision. |
| **Product repair** | AI working; product emerging. | Product-first route with an explicit AI application bridge. |

For a learner with two emerging foundations, recommend 30 days. If they choose
14 days, create a **dual-foundation starter**: cover the highest-leverage
foundations, label deeper topics as deferred, and state that the route provides
orientation and practice rather than full professional competence.

## Planning rules

1. Select topics from the learner's target role, evidence, highest-impact gap,
   usable domain experience, and timebox. Show both **selected** and
   **deferred** topics with a reason. Do not schedule every library topic by
   default.
2. Treat the five AI topic pools as the available library: model capability map
   and selection, RAG, Tool Calling, Agent, and Evals. Add system anatomy,
   context/output, AI UX/safety, observability, and integration only where they
   make a selected capability usable.
3. Keep progress separate:
   - **AI mainline** contains AI-specific capability and advances the AI-day
     counter.
   - **Product foundation** contains product framing, research, requirements,
     journeys, metrics, experiments, and delivery practices.
4. In Dual foundation mode, schedule one named outcome for each track every
   day. Pair them through a two-way bridge: how the product practice makes the
   AI decision useful or safe, and how AI changes the product practice.
5. Every active daily unit must name: capability, observable outcome,
   AI-specific delta or product decision, 1–3 key terms, familiar application,
   independent transfer check, and done condition.
6. The familiar project is a teaching anchor, not completion evidence. A
   different-domain or different-task-context scenario is required before
   recording Level 3 or above or advancing that unit.
7. For emerging foundations, retain the required knowledge card: terms, plain
   mechanism, boundary, and example. Adaptive pacing may skip optional depth,
   not these core elements.
8. Include one model capability map and selection unit in every selected route.
   In 14 days teach task categories and a role-relevant selection method; in 30
   or 60 days add representative evaluation, routing, fallback, and
   re-evaluation design. Verify dynamic provider facts from current official
   sources on the day of teaching.
9. Do not let generic product material consume an AI-mainline day. Preserve the
   named bridge between tracks. A real case, prototype, or build is optional
   laboratory work after the relevant concepts are understood.

## Minimum dual-foundation starter coverage

When the learner selects 14 days with two emerging foundations, use this as a
planning spine, then adapt the examples and order:

| Product foundation | AI mainline |
|---|---|
| User problem, target user, and success hypothesis | System anatomy and model boundary |
| Evidence, assumptions, and requirement scope | Context, prompts, and structured output |
| User flow and decision table | Model capability categories and selection |
| Source of truth and information architecture | RAG need, retrieval boundary, freshness |
| Service recovery and operational ownership | Tool Calling, Agent state, retries, handoff |
| Metrics, experiments, and release decisions | Evals, observability, AI UX, safety |

Use the remaining days for spaced review, role-relevant cases, independent
transfer, a target-JD evidence map, and one unseen integration challenge. Do
not present this table as exhaustive product or AI training.

## Output

Return the route in chat first, then save the accepted plan in one readable
Markdown file when the workspace is writable. Include:

1. selected duration, target role family, foundation profile, and learning mode;
2. personalization basis and explicit assumptions;
3. selected and deferred topics;
4. a two-track map, including which progress counter each item changes;
5. for every planned day:

   ```markdown
   ### Day N — [mode]
   **Product foundation unit:** outcome, key terms, and done condition
   **AI mainline unit:** outcome, AI-specific delta, key terms, and done condition
   **Bridge:** the shared product decision
   **Anchor application:**
   **Independent transfer check:**
   **System-map update:**
   **Optional deepening:**
   ```

   In AI bridge or product repair mode, mark the lighter track as a bridge
   rather than inventing a full unit.

6. initial durable-state fields: foundation profile, mode, both-track progress,
   mastery evidence, review points, anchor scenario, and next action; and
7. a handoff to `adaptive-ai-learning-coach`.

When the learner selects Chat-first plus milestone Markdown or Document-first,
use the matching existing system-map template in a single editable sprint-plan
file after the route is accepted. Do not create a file per lesson.
