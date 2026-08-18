# AI Product Career Learning

A skills-only plugin for people who want to transition into AI-related design, UX, product, agent, or experience roles, or build AI-product knowledge systematically. It turns a learner's real background, target role requirements, and learning preferences into a personalized route, then supports dialogue-first learning with visible progress.

## What this plugin includes

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

## User-facing output and durable state

The default is **Chat-first + milestone Markdown**:

- Teach, question, and collaborate in chat.
- Create editable workspace files only after a confirmed diagnosis, accepted sprint, meaningful learning checkpoint, accepted case, or accepted interview package.
- Let the learner inspect and correct every handoff before another Skill uses it.
- Use compact Markdown cards and tables by default; use diagrams only when relationships are genuinely hard to follow in text.

| Stage | User-facing output | State carried forward |
|---|---|---|
| Diagnosis | Direction, evidence map, proof map | Learning Handoff |
| Sprint plan | Personalized route and completion criteria | Learning state |
| Dialogue learning | Explanation, application feedback, progress | Updated learning log |
| Case strategy | Case analysis and story | Optional Case Handoff |
| Interview positioning | Interview narrative and answers | No required handoff |

## Language and localization

The canonical Skill instructions are English. The plugin replies and generates learner artifacts in the user's language. Technical terms may retain their common English acronym after a plain-language first explanation. Localized templates and documentation can be added without duplicating Skill logic.

## Privacy and factual integrity

- Do not commit real resumes, learning logs, interview transcripts, contact information, credentials, or employer-confidential material.
- Use anonymized examples only.
- Keep direct contribution, team contribution, observation, hypothesis, and prototype claims distinct.
- Do not represent model output as verified business fact.

## Plugin structure

```text
.codex-plugin/plugin.json
skills/
  ai-career-transition-planner/
  ai-career-sprint-plan/
  adaptive-ai-learning-coach/
  ai-career-case-strategy/
  ai-career-interview-positioning/
```

This is a skills-only plugin. During development, install and test it through a local plugin marketplace. For distribution, publish the repository and then package or submit the plugin according to the host's current plugin workflow.

## License

Distributed under the [MIT License](LICENSE).
