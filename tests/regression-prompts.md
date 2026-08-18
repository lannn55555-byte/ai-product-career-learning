# Regression prompts

Use these prompts to test the portable Skills in a new conversation before a release. Check the response against the stated expected behavior without providing the expected behavior to the Skill.

1. **Dialogue before project**
   - Prompt: "I want to learn AI product design. Do not make me build a project first. Start by teaching me."
   - Check: The coach starts with a concept and does not demand project context.

2. **Nonlinear RAG deep dive**
   - Prompt: "While learning RAG, explain embeddings and cosine similarity in detail."
   - Check: The coach marks a deep dive, answers it plainly, and does not advance the day counter.

3. **Parallel tracks**
   - Prompt: "I want AI learning and product foundations in parallel."
   - Check: The plan shows independent progress and an explicit bridge between paired topics.

4. **Prior answer recognition**
   - Prompt: "I already answered that earlier."
   - Check: The coach uses the earlier answer instead of repeating the same question.

5. **High-risk action reasoning**
   - Prompt: "Design an agent that cancels a hotel order after user confirmation."
   - Check: The response separates query and execution, requires backend revalidation, confirmation, idempotency, and persistent state.

6. **Language preference**
   - Prompt: "Explain in plain Chinese. Do not make it shorter just for the sake of being short."
   - Check: The response remains complete, direct, and free of decorative jargon.

7. **No writable workspace**
   - Prompt: "I am using a chat app that cannot save files. Start a learning session and keep my progress."
   - Check: The coach uses chat normally and returns a clearly named, copyable Markdown state block at meaningful checkpoints instead of assuming file access.

8. **Localized learner artifact**
   - Prompt: "Create a Chinese Learning Handoff from this confirmed diagnosis."
   - Check: The response uses the `zh-CN` template and does not mix English and Chinese labels in the same artifact.

9. **System model before glossary**
   - Prompt: "Teach me what an AI agent is. I have never learned AI product design."
   - Check: The coach first locates the agent in a shared AI-product system model and distinguishes model, knowledge, tools, state, rules, and human handoff. It does not present an agent as a standalone model feature.

10. **Spiral revisit and mastery evidence**
   - Prompt: "We learned retrieval yesterday. Today we are learning tool calling. Why are they different?"
   - Check: The coach compares facts versus actions, revisits the shared scenario, records node-level mastery evidence, and asks a fresh decision question rather than repeating a definition.

11. **Integration and transfer**
   - Prompt: "I finished the foundation sprint. Give me the final challenge."
   - Check: The coach gives an unseen scenario and asks for user problem, selected/excluded components, source of truth, tool boundaries, rules, state, confirmation, handoff, user control, metrics, and a trade-off. It does not equate completion with job readiness.

12. **Mechanism deep dive**
   - Prompt: "I understand that RAG retrieves information, but why can it find similar wording? Explain embeddings and cosine similarity from the mechanism level."
   - Check: The coach treats this as a branch, explains the mechanism plainly, reconnects it to retrieval design choices, and does not advance the day merely because the deep dive occurred.
