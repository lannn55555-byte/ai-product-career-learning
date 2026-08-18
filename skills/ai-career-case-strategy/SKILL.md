---
name: ai-career-case-strategy
description: Analyze one real project and turn it into a factual, interview-ready AI-related case with claim boundaries, product trade-offs, evidence gaps, and a two-minute story. Use when a user asks to analyze a project, portfolio case, workflow, product feature, automation, or personal proof of concept for an AI-related career transition.
---

# AI Career Case Strategy

## Scope

Analyze one case at a time. Return only that case's evidence, claim boundary, product reasoning, and story. Do not create a career diagnosis or a full learning plan.

## Intake

Collect the minimum facts:

- business goal and user;
- original process or problem;
- user's exact contribution;
- tools, rules, AI, and human roles;
- verified outcome, observation, or limitation;
- hardest decision or trade-off.

Ask only for facts that change what the user can truthfully claim.

## Analysis

1. Classify each statement as direct contribution, team contribution, observation, hypothesis, or personal prototype.
2. Identify the product problem, alternatives, decision, risk, measurement, and next iteration.
3. For AI-related work, distinguish deterministic rules, model work, human review, fallback, quality/latency/cost trade-offs, and data/permission boundaries.
4. Identify one evidence gap that can be cheaply filled when needed. Do not recommend building a large demo.

## Output

### User-facing output

Return only:

1. Case title and one-sentence value.
2. Evidence table and claim boundary.
3. Product decision and AI-system reasoning.
4. Two-minute story.
5. Likely follow-up questions with factual answers.
6. One minimal evidence improvement, if needed.

Present the analysis in chat first. Create one editable case-card Markdown artifact only after the user accepts the case framing or chooses a document-oriented output mode. Use a visual only for a process, evidence map, or trade-off that is materially clearer as a diagram.

### Handoff to interview positioning

When the user is preparing for an interview, append a concise `Case Handoff`: case title, claim boundary, user's exact contribution, verified outcome or limitation, key product/AI decision, and two-minute story. Show it to the user and save it as optional input for `$ai-career-interview-positioning`. Do not turn observations or hypotheses into verified outcomes.
