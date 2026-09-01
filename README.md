# AI Product Career Learning

A portable collection of Agent Skills for people who want to transition into AI-related design, UX, product, agent, or experience roles, or build AI-product knowledge systematically. It turns a learner's real background, target role requirements, and learning preferences into a personalized route, then supports dialogue-first learning with visible progress.

The source of truth is the standard `skills/<skill-name>/SKILL.md` structure.

## What this toolkit includes

| Skill | Use it for | Main output |
|---|---|---|
| `ai-career-transition-planner` | Career direction and evidence diagnosis | Role-family fit, proof map, gaps, Learning Handoff |
| `ai-career-sprint-plan` | Personalized learning route | AI-mainline and product-foundation plan, learning state |
| `adaptive-ai-learning-coach` | Start or continue learning | Dialogue teaching, applications, progress, updated learning log |
| `ai-career-case-strategy` | Turn one project into credible evidence | Case analysis, claim boundary, two-minute story |
| `ai-career-interview-positioning` | Interview preparation | Positioning, answers, concerns, interviewer questions |

## Typical routes

```text
Career transition
→ Career diagnosis
→ Personalized sprint plan
→ Dialogue learning
→ Case strategy (when needed)
→ Interview positioning (when needed)

Systematic learning without a career goal
→ Sprint plan with provisional assumptions
→ Dialogue learning
→ Recalibrate later when a role target or JD is available
```

The tracks are distinct but connected. The AI mainline covers model boundaries, context, RAG, tools, agents, evaluation, AI UX, and safety. Product foundations cover problem framing, research, metrics, workflows, and decision rules. Users can choose parallel, foundation-first, or AI-first sequencing.

The MVP supports 14-, 30-, and 60-day learning routes; when no duration is stated, it recommends 14 days. Its initial library covers model capability map and selection, RAG, Tool Calling, Agent, and Evals, but the route selects and orders topics from the learner's profile, target role, current evidence, and timebox rather than making every learner complete a fixed list. Every route includes a scoped model-selection unit; the 30- and 60-day routes add spaced practice, role specialization, and optional evidence-building. No route is a glossary or a job-readiness promise. It starts with one shared AI-product system model—model behavior, context, knowledge, tools, state, user control, and evaluation—then revisits an anchor scenario as each component is learned. It prioritizes procedural capability: notice a cue, choose an action, explain the boundary, and revise the action when conditions change. The final task uses an unseen scenario to test transfer, not recall.

Every AI-mainline lesson identifies its AI-specific delta before teaching: a model, retrieval, tool, or state mechanism; a new failure mode; or a new design responsibility beyond the paired product-foundation practice. General product, UX, metrics, and QA lessons stay on the product-foundation track unless that delta is explicit. The evaluation module distinguishes deterministic QA, product measurement, AI Evals, and live-request observability.

Lesson-source selection and factual-claim rules live in [the learning evidence and source policy](skills/adaptive-ai-learning-coach/references/learning-evidence-and-source-policy.md).

Application prompts state known facts, decision scope, and expected output. Feedback preserves a learner's stated qualifiers and treats extra edge cases as follow-up depth unless they change the current conclusion.

## User-facing output and durable state

The default is **Chat-first + milestone Markdown**:

- Teach, question, and collaborate in chat.
- Create editable workspace files only after a confirmed diagnosis, accepted sprint, meaningful learning checkpoint, accepted case, or accepted interview package. If the host has no writable workspace, return a clearly named Markdown block for the learner to copy and retain.
- Let the learner inspect and correct every handoff before another Skill uses it.
- Use compact Markdown cards and tables by default; use diagrams only when relationships are genuinely hard to follow in text.

| Stage | User-facing output | State carried forward |
|---|---|---|
| Diagnosis | Direction, evidence map, proof map | Learning Handoff |
| Sprint plan | Personalized route, system map, and mastery targets | Learning state |
| Dialogue learning | Explanation, application feedback, system-map updates, and progress | Updated learning log |
| Case strategy | Case analysis and story | Optional Case Handoff |
| Interview positioning | Interview narrative and answers | No required handoff |

## Install and use

Use an Agent Skills-compatible coding agent or runtime. For tools that support `skills.sh`, install one Skill at a time, for example:

```bash
npx skills add lannn55555-byte/ai-product-career-learning --skill adaptive-ai-learning-coach
```

Choose the Skill that matches the learner's current need. A typical route is diagnosis -> sprint plan -> dialogue learning; case strategy and interview positioning are optional later stages.

Each Skill is self-contained. Discovery, installation commands, and available file or tool access vary by host, so verify that the host has found the installed Skill.

### Browser chat products

Browser-chat products do not use the same local Skill installation flow as coding agents. Use the host's native customization format where available (for example, a Gem or custom instructions). A GitHub link may provide temporary reading context, but its behavior varies by host.

## Language and localization

Canonical Skill instructions and agent-facing references are English. User-facing templates and examples are separated by language: `en/` and `zh-CN/`. Choose the matching folder for the learner's language; do not mix languages inside one artifact. Technical terms may retain their common English acronym after a plain-language first explanation.

## Examples

Examples are for people reading the repository; Skills do not load them as instructions.

- [English career-diagnosis output](docs/examples/en/career-diagnosis-output.md)
- [中文职业诊断输出](docs/examples/zh-CN/career-diagnosis-output.md)
- [English role-translation patterns](docs/examples/en/role-translation-patterns.md)
- [中文职业转化模式](docs/examples/zh-CN/role-translation-patterns.md)

## Privacy and factual integrity

- Do not commit real resumes, learning logs, interview transcripts, contact information, credentials, or employer-confidential material.
- Use anonymized examples only.
- Keep direct contribution, team contribution, observation, hypothesis, and prototype claims distinct.
- Do not represent model output as verified business fact.

## Repository structure

```text
skills/
  ai-career-transition-planner/
  ai-career-sprint-plan/
  adaptive-ai-learning-coach/
  ai-career-case-strategy/
  ai-career-interview-positioning/
tests/
docs/
```

Each `SKILL.md` is canonical English.

## License

Distributed under the [MIT License](LICENSE).
