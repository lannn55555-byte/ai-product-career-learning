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
