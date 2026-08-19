# AI Product Learning Architecture

Use this reference to plan or teach the AI mainline. Treat it as a connected capability map, not a list of isolated topics. Read [learning-evidence-and-source-policy.md](learning-evidence-and-source-policy.md) to select source-grounded content and collect procedural learning evidence.

## Shared system model

Teach this model before or alongside the first AI-mainline module:

```text
User problem
  -> model behavior
  -> task context
  -> external knowledge
  -> tools and backend actions
  -> state, rules, and human handoff
  -> user control and recovery
  -> evaluation and observability
```

Not every product needs every component. The learner must explain why a component is needed, what owns the source of truth, and what should remain deterministic.

## Learning target: procedural capability

The primary target is not semantic recall of terms. It is the ability to notice a situation, choose an appropriate product action, explain why it fits, recognize its boundary, and adapt when the situation changes. Use terms only as labels that make this procedure easier to communicate.

Record each durable insight in this form:

```text
When [cue], choose [action or design rule], because [mechanism or constraint];
do not do this when [boundary]; verify through [observable result].
```

## Capability map

| Node | Core question | Depends on | Demonstrated mastery |
|---|---|---|---|
| System anatomy | What components does this AI product need, and why? | None | Map a user request to needed and unnecessary components. |
| Model boundary | What can a probabilistic model do, and what must remain a rule or human decision? | System anatomy | Separate interpretation/generation from deterministic policy and irreversible action. |
| Context and output | What information and format make one model step reliable enough? | Model boundary | Define inputs, output schema, missing-information behavior, and validation. |
| Knowledge and retrieval | Which external facts are needed, who owns them, and how are freshness and permission protected? | Context and output | Choose sources and retrieval boundaries; identify when retrieval is unnecessary. |
| Tools and actions | What must be queried or executed outside the model? | Model boundary, context | Separate read queries from execution; specify backend revalidation and confirmation. |
| State and orchestration | What stage is the task in, what is next, and when should it stop or hand off? | Tools and actions | Design state, transitions, retries, idempotency, and handoff. |
| AI UX and safety | How does the user understand, control, correct, or recover from uncertain behavior? | Model boundary, state | Design confirmation, provenance, fallback, and recovery. |
| Evaluation and observability | Did the system solve the user problem, and where did it fail? | All earlier nodes | Define task success, system-quality checks, logs, and a next experiment. |
| Integration and transfer | Can the learner apply the model to a new domain? | All earlier nodes | Decompose an unseen scenario and defend the component choices. |

## Technical exposure and depth

Do not expect learners to request terms they have never encountered. Introduce the necessary technical idea when its system node is first taught, then control depth rather than hiding the idea.

1. **Awareness:** Proactively name the mechanism, its purpose, and one plain-language analogy. Every learner receives this level. Example: `Embeddings turn text meaning into positions so retrieval can look for nearby meanings.`
2. **Working mechanism:** Explain the part that changes a product decision. Every learner receives this level when the matching node is taught.
3. **Deep mechanism:** Expand the implementation-level explanation when the learner asks, the target role needs it, or a probe/application reveals a mechanism-level gap or misconception.

Never ask a novice whether they want to learn an unknown term before establishing why it matters. Do not require advanced mathematics before product reasoning. Use a short diagnostic or transfer question to decide whether to open the deep-mechanism branch, then reconnect it to the decision it changes.

| Topic | Awareness and working mechanism | Deep mechanism | Usually optional for product decisions |
|---|---|---|---|
| Model behavior | Tokens are processed in context; generated output is probabilistic and bounded by instructions and context. | Next-token prediction, probability distributions, temperature, attention and context-window trade-offs. | Training objectives, gradient descent, parameter optimization. |
| Embeddings and retrieval | Text can be represented for meaning-based retrieval; retrieval quality depends on sources, chunks, ranking, freshness, and permissions. | Vector representations, cosine similarity, chunking, hybrid search, reranking. | Deriving vector training losses or implementing an index from scratch. |
| Structured output and tools | The model proposes structured data or a tool call; deterministic systems validate and execute. | Schemas, constrained decoding, function-calling loops, API contracts. | Building a model-serving stack. |
| Agent orchestration | Multi-step tasks need state, policies, tool boundaries, and recovery. | Planning loops, memory types, routing, retry policies, idempotency. | Training a custom agent model. |

Treat a learner-requested deep dive, a role requirement, or a revealed mechanism-level gap as a branch. Explain the mechanism, then reconnect it to the product decision the mechanism changes.

## Mastery levels

Track each node independently. Do not infer mastery from time spent, term recall, or a correct answer on the anchor scenario alone.

| Level | Meaning | Evidence |
|---|---|---|
| 0 — Unseen | The learner has not encountered the node. | None. |
| 1 — Recognize | The learner can identify the node in an explained example. | Names its purpose correctly; this is orientation, not completion. |
| 2 — Explain | The learner can explain why it exists and its boundary. | Plain-language explanation plus one limitation. |
| 3 — Decide | The learner can choose whether and how to use it in a scenario. | States a cue, defends a design choice, and rejects an unsuitable option. |
| 4 — Design | The learner can combine it with adjacent nodes in a concrete flow. | Produces a coherent flow, rule, schema, or evaluation plan with a verification step. |
| 5 — Transfer | The learner can apply the system model to an unfamiliar domain and revise after critique. | Solves a new scenario, explains trade-offs, and changes the procedure when conditions change. |

## Spiral learning rules

1. Start with one anchor scenario drawn from the learner's domain when useful; otherwise use a neutral service-change scenario.
2. Before introducing terminology, ask the learner how they would solve the scenario now. Preserve that baseline.
3. Revisit the same scenario when each new node is learned. Mark what changed in the system map and why.
4. Use a fresh scenario after several nodes. Do not reuse the anchor as the only proof of understanding.
5. Record the node, mastery level, evidence, misconception or uncertainty, and next review point.
6. Use the procedure loop: scenario cue -> learner decision -> mechanism -> feedback -> changed scenario -> revised decision. Space a later retrieval of the same decision rule.

## Aha checks

Use these checks to test whether connections—not vocabulary—are forming:

- After system anatomy: Can the learner see why "use a model" is not a complete product design?
- After knowledge and tools: Can the learner distinguish facts the model needs from actions the system must perform?
- After state and safety: Can the learner explain why a helpful response does not authorize an irreversible action?
- At integration: Can the learner receive one natural-language request and derive model, knowledge, tools, rules, state, UX, and evaluation choices?

## Integration challenge

Use an unseen, role-relevant scenario. Ask the learner to:

1. state the user problem and success condition;
2. select needed components and explicitly exclude unnecessary ones;
3. define source-of-truth data, tool boundaries, and deterministic rules;
4. define state, confirmation, fallback, and human handoff;
5. define user control and recovery;
6. define one task-success metric and one system-quality metric; and
7. name one important trade-off.

Score the response by mastery evidence, not by whether it uses every term.
