# AI mainline and product-foundation bridges

Keep the tracks separate for progress, but pair them through a concrete design question.

| AI mainline | Product foundation | Two-way connection |
|---|---|---|
| Model limits, prompting, structured output | User problem and hypothesis | A hypothesis identifies the outcome that matters; model limits determine whether AI can contribute reliably. |
| RAG and data sources | Research, source of truth, information architecture | Research identifies facts users need; RAG design decides which sources, freshness, permissions, and structure can support them. |
| Tool Calling and APIs | Service blueprint, decision table, operational policy | The product flow identifies facts, decisions, owners, and exceptions; tools and backend rules make those steps executable and safe. |
| Agent routing and state | Journey mapping and service recovery | A journey identifies stages and failure points; state and routing determine allowed actions and recovery at each stage. |
| Evaluation and observability | Metrics, research, and experimentation | Product metrics locate a behavior or outcome change; AI evaluation identifies whether model, retrieval, tools, or workflow caused it. |
| AI UX | Interaction design and trust | Product UX defines understandable choices; AI UX additionally communicates uncertainty, provenance, controllability, and limits. |
| Safety and human oversight | Risk, permissions, and policy design | Product policy defines accountable boundaries; AI systems require those boundaries across model, tools, and human handoff. |

In Parallel mode, choose the row aligned with the current AI module. In sequential modes, retain the bridge note and use it as the opening connection when the second track begins.
