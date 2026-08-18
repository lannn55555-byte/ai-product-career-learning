---
name: ai-career-sprint-plan
description: Plan a personalized AI-career learning sprint from a verified Learning Handoff or available learner profile, with a choice between AI-mainline-only, product-foundation-first, or parallel tracks. Use when a user asks for a learning plan, study schedule, 10-day sprint, or learning roadmap for AI product design, AI UX/UI, AI experience design, AI application product, agent design, or related AI roles.
---

# AI Career Sprint Planner

## Scope

Create the learning route and initialize durable learning state. Do not teach the lessons, force a project, or turn the first interaction into a task interview. Actual multi-turn teaching belongs to `adaptive-ai-learning-coach`.

Read a verified Learning Handoff when available. Otherwise use the accepted diagnosis and relevant learner information: target role, experience, domain assets, AI-specific gaps, prior familiarity, target JD, public-project constraints, learning preferences, and accessibility preferences. Do not repeat the full diagnosis or ask for information already available. If no diagnosis exists, create a provisional route, label its assumptions, and create a provisional handoff for later recalibration.

## Intake

Ask only when unknown and material:

1. Is there a deadline or preferred sprint length? Default to 10 learning days.
2. Which track sequence does the learner prefer?
   - **Parallel:** each learning day includes an AI-mainline block and a product-foundation block.
   - **Foundation first:** complete the product foundation before starting the AI mainline.
   - **AI first:** complete the AI mainline first, then add foundations.

Study hours are optional calibration information, never a prerequisite to starting. If unknown, use flexible blocks rather than demanding an estimate.

## Personalization Rules

- Prioritize capabilities that close the learner's highest-impact, realistically closable gaps for the target role family.
- Use existing domain knowledge as a teaching bridge and optional application material, without requiring a project narration before learning starts.
- Adapt depth and application difficulty to demonstrated knowledge. If the learner already understands a module, test its boundary or move forward instead of reteaching definitions.
- Preserve explicit preferences about language, pace, progress visibility, output mode, and nonlinear exploration.
- State the personalization basis briefly: `Built from: [target + strengths + priority gaps + learning preferences]`.

## Planning Rules

- Keep two independently visible tracks when foundations are included:
  - **AI mainline:** AI-specific capability; this alone advances `Day N / 10`.
  - **Product foundation:** problem framing, hypotheses, research, metrics, decision tables, and related product skills; it has separate progress and never silently consumes an AI day.
- Keep the tracks distinct for progress but connect them deliberately. For every AI module, name the related product foundation and explain both directions: how the foundation makes the AI decision useful or safe, and how AI changes the product-design question.
- In Parallel mode, pair each AI block with its most relevant foundation block. In sequential modes, retain the bridge note for the later handoff. Read [../adaptive-ai-learning-coach/references/track-bridges.md](../adaptive-ai-learning-coach/references/track-bridges.md) when selecting pairs.
- Default AI mainline: model boundaries → context/prompt/structured output → RAG/data sources → Tool Calling/API/workflows → agents/routing/state → evaluation/observability → AI UX → safety/human oversight → end-to-end design.
- Allow side questions to deepen a topic without advancing the day counter until that day's outcome is met.
- Treat a real project, case, or prototype as an optional laboratory after the relevant concept is understood.
- Use scenario-based applications, not definition drills.

## Output

### User-facing output

Return:

1. Sprint scope, target role family, and chosen track sequence.
2. Personalization basis: target, usable strengths, priority gaps, familiarity, and preferences used.
3. A concise map of both tracks, marking what counts toward the AI-mainline total and the bridge between tracks.
4. For each AI day:

```markdown
### Day N — [AI mainline topic]
**Why it matters:**
**Main outcome:**
**Product connection:**
**Dialogue sequence:** concept → mechanism → boundary → connection → application
**Product-foundation block:** [topic or queued]
**Done when:**
```

5. A learning-state initialization section.
6. One handoff to `adaptive-ai-learning-coach`.

Present the route in chat first. When the learner selects `Chat-first + milestone Markdown` or `Document-first`, save one editable sprint-plan file after the route is accepted. If the host has no writable workspace, return one clearly named Markdown block for the learner to copy and retain. Do not create a separate file for every lesson. Use a compact table or progress card for track comparison; use a diagram only when it clarifies cross-track dependencies.

### State for the next Skill

Save or update a workspace learning state when possible. Otherwise return a named, copyable learning-state Markdown block. Show it briefly to the learner, then make it available to `adaptive-ai-learning-coach`. Include only: verified Learning Handoff summary, selected track sequence, AI-mainline and foundation maps/progress, active day, branch status, completed outcomes, unresolved questions, and one next step. Do not pass the full diagnosis or raw conversation by default.
