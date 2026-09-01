# Model Landscape and Project Selection

Use this reference for the core model-capability-map and selection unit, and whenever the learner asks to compare current models. Every selected route includes a scoped version of this unit; it may be an orientation in a short route or a comparative evaluation in a longer route. It complements, but does not replace, the learner's selected RAG, Tool Calling, Agent, or Evals learning. It defines a teaching and decision process; it does not freeze a fast-changing vendor ranking.

## What must be compared first

Start with two maps, then move to a project decision.

1. **Horizontal map — across providers:** compare current model families against the task categories that matter: reasoning, coding and Agent work, long-context work, creativity, multimodal understanding/generation, voice, retrieval/reranking, and image/video/3D.
2. **Vertical map — within one provider:** distinguish flagship/high-quality, balanced/fast, and specialist offerings. A model family can have different strengths at each tier; the provider name alone is not a useful choice.

Use this plain distinction:

| Term | Plain definition | Not the same as |
|---|---|---|
| General-purpose model | One model intended to handle many kinds of language, reasoning, code, or multimodal tasks. | A business workflow with tools and rules. |
| Specialist model | A model optimized for a narrower technical job, such as speech recognition, embeddings, reranking, image generation, video, 3D, moderation, or code. | A specialist Agent. |
| Specialist Agent | A product-level worker for one business domain. It may use one or several general-purpose and specialist models, plus tools, policies, state, and human handoff. | A model by itself. |
| Model routing | Sending different task types or risk levels to different models under explicit rules. | Letting a model freely choose every provider or tool. |

Do not teach a subjective claim such as “Model X is more creative” as a stable universal fact. State its evidence class and scope: task, language, prompt, tools, model version, and date.

## Evidence classes

Every meaningful comparison must be labelled:

| Evidence class | What it can support | What it cannot support alone |
|---|---|---|
| Current official product fact | Model names, documented modalities, API features, limits, pricing, availability, data-processing terms, and deprecation notices. | A claim that it gives the best answer for this product. |
| Learner or operator observation | A concrete experience such as “this model made frontend work easier in my setup.” | A broad benchmark or permanent vendor ranking. |
| Comparative evaluation result | A result on representative tasks with recorded version, configuration, and metrics. | A conclusion beyond the sampled tasks or date. |

Use current official provider sources on the day of teaching for any dynamic fact. Record the source URL, access date, model/version identifier, and the relevant deployment region where applicable. Do not use provider marketing wording as proof of task quality.

## Project-selection sequence

1. **Define the job, not the brand.** What must the system understand or produce? Is the task creative, deterministic, multi-step, real-time, multimodal, high-risk, or compliance-bound?
2. **Set hard constraints.** Examples: supported modality, region/data handling, maximum P95 latency, budget unit, required context/output length, Tool Calling or structured outputs, version stability, and safety boundary.
3. **Create a short candidate map.** Include general-purpose candidates and, when the task needs one, specialist models. Do not assume a general model replaces speech, embedding, reranking, image/video/3D, or moderation components.
4. **Run a small evaluation.** Use representative cases and score task quality, safety/groundedness, tool or schema reliability, P95 latency, and end-to-end cost. Include failure cases, not only successful demos.
5. **Choose operating design.** Select a default model, optional router, fallback, user-facing degradation behavior, and a human handoff where risk requires it.
6. **Set a review trigger.** Re-evaluate when the model/version changes, the prompt or tools change, source data shifts, performance regresses, cost/latency crosses a limit, or the task distribution changes.

## Teaching order

Keep the learning load low:

1. Give the requested horizontal and vertical map using only the categories relevant to the learner's project question.
2. Explain one nearby distinction: specialist model versus specialist Agent, or model routing versus a single-model design.
3. Show the project constraints that remove unsuitable candidates.
4. Ask for a decision only after explaining the evaluation evidence needed to justify it.

The AI-specific delta is that model capability, availability, behavior, cost, and safety can all vary by provider, version, and configuration. Product requirements therefore become a repeatable comparative evaluation and operating-design problem, not a one-time brand preference.
