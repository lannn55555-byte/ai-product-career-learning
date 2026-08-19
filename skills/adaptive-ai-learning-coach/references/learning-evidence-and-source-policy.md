# Learning Evidence and Source Policy

Use this reference when selecting lesson content, making a factual technical claim, or judging whether a curriculum node has adequate evidence. This is a source-selection policy, not a document dump and not a substitute for checking current facts.

## Learning outcome

Prioritize procedural capability over vocabulary recall. A learner has useful evidence when they can recognize a scenario cue, choose or reject an action, explain the mechanism and boundary, then revise the choice in a changed scenario.

Use this evidence pattern:

```text
Cue -> decision or action -> why it fits -> boundary or exception -> result -> revised action
```

Definitions, diagrams, and source reading support this loop; they do not complete it. Require scenario practice, feedback, variation, and later retrieval before recording Decide, Design, or Transfer mastery.

## Source classes

| Class | Use for | Authority rule | Examples |
|---|---|---|---|
| Stable foundations | Mechanisms that change slowly | Prefer original research, standards, or primary technical sources. | [Attention Is All You Need](https://arxiv.org/abs/1706.03762); [RAG](https://arxiv.org/abs/2005.11401) |
| Risk and system practice | Safety, governance, evaluation, and lifecycle questions | Prefer standards bodies and research, then adapt to the actual product context. | [NIST AI RMF](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10); [NIST Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) |
| Current platform behavior | API schemas, model features, pricing, limits, and provider-specific workflows | Use the provider's current official documentation and record its access date. Never generalize it to all providers without support. | [Function calling](https://developers.openai.com/api/docs/guides/function-calling); [File search](https://developers.openai.com/api/docs/guides/tools-file-search); [Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs); [Evals](https://developers.openai.com/api/docs/guides/evals) |
| Role evidence | What a learner needs for a particular job family | Prefer supplied target JDs, portfolio requirements, and interview feedback. Date and label job-market samples. | User-provided JD, recruiter feedback, public job posting |
| Community and open evidence | Recent interview themes, practitioner vocabulary, and scenario ideas | Treat as a dated, unverified signal. Triangulate before making a hiring claim; never use it alone for technical fact or company policy. | Forum discussion, public interview report, practitioner post |
| Learning-method evidence | Teaching and assessment design | Prefer educational research; do not overstate what one study proves. | [Karpicke & Blunt (2011)](https://pubmed.ncbi.nlm.nih.gov/21252317/) on retrieval practice and meaningful learning |
| Learner evidence | Personalization and mastery decisions | Treat the learner's verified experience and scenario answers as the primary source. | Confirmed background, prior answer, artefact, feedback |

## Node-to-source routing

| Capability node | Minimum source basis | Practice evidence to collect |
|---|---|---|
| Model boundary and context | Stable foundation; current provider docs only for current behavior | Separate a probabilistic interpretation task from a rule or human decision. |
| Knowledge and retrieval | RAG foundation; current retrieval documentation when implementation matters; user domain sources | Select a source of truth, freshness rule, permissions, and retrieval/no-retrieval decision. |
| Tools and actions | Current official tool/API documentation plus the product's backend contract | Separate query from execution; specify confirmation and backend revalidation. |
| State and orchestration | Stable engineering patterns plus current provider docs only when provider behavior matters | Draw states, transitions, retry/idempotency behavior, stop rule, and handoff. |
| AI UX and safety | Risk source plus actual user/task context | Design uncertainty display, correction, recovery, and an unsafe-action boundary. |
| Evaluation and observability | Evaluation source plus product metrics definitions | Define a task-success measure, a system-quality measure, and a diagnostic follow-up. |

## Selection and update rules

1. Start with the capability node and decision the learner must make; do not start from a fashionable term or one vendor's feature.
2. Record every non-trivial source as: URL or citation, source class, publication/update date when available, and verification date. Mark claims as **stable**, **current**, **role-specific**, **community signal**, or **learner-specific**.
3. When a provider source conflicts with a stable foundation, teach the distinction: the provider document describes one implementation; it does not replace the underlying principle.
4. Use no source merely to make a lesson look authoritative. State what the source changes in the learner's design decision.
5. Verify platform behavior, model availability, pricing, limits, policies, and APIs on the day the claim is used when tools are available. Do not reuse an old summary as current fact.
6. Prefer recent role-market and community evidence. If an item is older than the learner's target hiring cycle, has no date, or conflicts with a newer primary source, label it historical/low-confidence or exclude it.
7. Use community evidence to create scenario practice, identify hypotheses, or ask better follow-up questions. Require a target JD, official company material, multiple independent recent reports, or direct interview feedback before stating a company-specific interview expectation.
8. Maintain a short, versioned source list. Review current-platform links before a release or when the learner relies on a product claim.

## Teaching sequence

For each lesson, use: scenario cue -> learner's first decision -> just-enough source-grounded mechanism -> revised decision -> variation -> delayed retrieval. Ask for a term definition only when it helps diagnose a mistaken decision, never as the default completion test.
