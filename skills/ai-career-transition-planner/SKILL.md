---
name: ai-career-transition-planner
description: Analyze a professional's real experience and recommend a primary AI-related role family plus up to two adjacent directions, with evidence-based fit, capability gaps, a Career Proof Map, and a verified learning handoff. Use when someone wants to transition into or grow toward AI product design, AI experience design, AI UX/UI, AI application product, agent or conversational design, or another AI-adjacent non-engineering role.
---

# AI Career Proof Mapper

## Scope

Run the core career diagnosis only. Return role-direction analysis, evidence, domain assets, gaps, one shareable Career Proof Map, and one suggested next action. Do not create a study plan, deep-dive a case, or write interview answers unless the user explicitly asks. Read [references/diagnosis-quality-rubric.md](references/diagnosis-quality-rubric.md) before finalizing.

Reply in the user's language. Preserve factual integrity: distinguish direct contribution, team contribution, observation, hypothesis, and personal prototype. Never invent ownership, metrics, launch results, or a target role the user did not support.

## First-use evidence onboarding

When the workspace contains this learning-agent project and a career diagnosis
starts, its materials are requested, or the project is introduced, if
`retrieve_aipm_evidence` is unavailable, do not expect the user to ask for RAG
or citations. Proactively offer the included local reference library in plain
language. Explain that it downloads third-party material and a local embedding
model, creates local project files, and adds one local retrieval tool to Codex;
then end the same response with a direct question asking whether to enable it.
Never merely say that the library is optional or unavailable before moving on
to request a resume or other intake material.

Only after the user explicitly agrees to the AIPM-Wiki terms described in
`THIRD_PARTY_NOTICES.md`, run the project setup flow and ask them to start a
new task. If they decline, still complete a resume-based diagnosis, but label
role guidance as a framework-based inference rather than cited external
evidence. If this project is not present in the workspace, do not invent a
setup command or imply that a knowledge base is enabled.

If the user asks to use their own material, do not default to AIPM-Wiki. Follow
the project policy for a custom knowledge base: request a local folder of
Markdown, TXT, PDF, or DOCX files and rights confirmation; explain that it
becomes the active library rather than merging with the default source.

## Intake

Use a resume, career profile, work history, project notes, interview feedback, or target JD. Collect or infer:

- target role family, role title, target companies, or broad direction;
- public projects and the user's exact role;
- target JD when available;
- constraints that affect credible claims or portfolio use.

Ask at most two questions, and only when the answer would materially change the diagnosis. Do not ask about study hours or a schedule here.

## Diagnosis Workflow

### 1. Compare role directions

- Recommend one primary direction and up to two adjacent directions only when the evidence supports them.
- Interpret role titles through their actual JD requirements. Do not assume a title such as "AI Designer" or "AI UX/UI Designer" means the same thing at every company.
- When a target role is known and tools are available, use dated public community interview reports only as supplementary signals for recent themes and mock-question design. Record their date and source type, match role/location where possible, and triangulate before making any company-specific claim.
- When a target JD and realistic time constraint are supplied, score each direction with a **Path Fit Score** out of 100. It is a prioritization aid, not a hiring probability.
- When either is missing, show only an **Evidence Readiness Score** out of 60. Never invent a JD or time constraint merely to produce a total.

| Score component | Weight | Evidence |
|---|---:|---|
| Verifiable evidence | 35 | Strength, specificity, and ownership of relevant work. |
| Transferable and domain assets | 25 | Relevant domain data, SOPs, user insight, or workflow knowledge. |
| Target-role or JD fit | 25 | Match to a supplied JD; show `N/A` when absent. |
| Short-sprint closability | 15 | Whether high-impact gaps can be closed within the stated time; show `N/A` when unknown. |

`Evidence Readiness = Verifiable evidence + Transferable and domain assets.` State confidence: high with concrete evidence and a JD; medium with a role direction only; low when both are broad.

### 2. Map evidence, domain assets, and gaps

For each relevant capability, record context, exact role, method, verified outcome or limitation, and claim type. Identify useful domain assets: entities, fields, statuses, documents, exceptions, decision rules, approvals, handoffs, freshness, permissions, and sensitive-data constraints.

Use this coordinate system:

| Axis | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Evidence strength (X) | No evidence | Stated only | Small artifact | Personal decision/process evidence | Repeated or measurable proof | Strong, repeatable, externally verifiable proof |
| AI-specific gap (Y) | Can explain and apply | Minor polish | Practice needed | Core concept or method missing | Major capability gap | No relevant understanding or evidence |

Interpretation: lower-right = lead now; upper-right = translate first; lower-left = support; upper-left = defer unless required.

### 3. Apply the AI experience lens

Identify whether the user can explain:

- deterministic business rules versus probabilistic model behavior;
- quality, latency, and cost trade-offs;
- guardrails, fallback, evaluation, and human-in-the-loop boundaries;
- when domain information needs retrieval, deterministic rules, a tool call, or a human decision.

Do not call data "RAG-ready" without checking source of truth, freshness, permissions, and task need.

### 4. Create a Career Proof Map and diagnosis artifact

Use the matching-language templates: [English diagnosis template](templates/en/career-diagnosis.md), [Chinese diagnosis template](templates/zh-CN/career-diagnosis.md), [English proof map](templates/en/ai-career-proof-map.md), or [Chinese proof map](templates/zh-CN/ai-career-proof-map.md). Create a diagnosis artifact only after the user confirms that they want a milestone document. Keep the proof map to one screen or printed page when possible. Include only:

- primary role direction and score type;
- positioning statement;
- three proof points to lead with;
- two high-priority gaps; and
- one next action.

Do not make it decorative. Every element must link to factual evidence or a clearly labeled gap.

### 5. Select one next action

Choose exactly one next action and ask for confirmation before expanding:

- Need a personalized learning route → `ai-career-sprint-plan`.
- Need to turn one real project into evidence → `ai-career-case-strategy`.
- Need to prepare for a specific interview → `ai-career-interview-positioning`.

### 6. Create a verified Learning Handoff

When the next action is learning, use the matching-language [English Learning Handoff](templates/en/learning-handoff.md) or [Chinese Learning Handoff](templates/zh-CN/learning-handoff.md). Fill it only with diagnosis facts and the user's stated preferences. Show the concise card to the user for correction. Save it in a writable workspace when available; otherwise return it in a clearly named Markdown block that the user can copy into their preferred record.

The handoff is shared, user-verifiable state, not hidden reasoning. Do not pass a raw conversation transcript or invent missing fields.

## Presentation Contract

Present the diagnosis in chat first, using compact headings and tables when useful. After the learner confirms a stage, create or update an editable Markdown artifact only when their output mode includes milestone documents. If the host has no writable workspace, return a copyable Markdown block instead. Use a visual card or diagram only when it clarifies a map, comparison, or relationship better than text; never replace editable facts with an image.

## Output

Return only:

1. Role directions and applicable Evidence Readiness or Path Fit Scores.
2. Positioning statement.
3. Evidence, domain-asset, and capability coordinate map.
4. Three priority gaps and claims to avoid.
5. Career Proof Map.
6. One recommended next Skill and a concise reason.
7. Learning Handoff when the next step involves learning.
