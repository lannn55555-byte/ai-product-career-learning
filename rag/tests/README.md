# Retrieval acceptance set

## Cross-language acceptance set

`cross_language_acceptance_cases_v1.jsonl` contains English questions whose
expected evidence remains in the Chinese AIPM-Wiki corpus.
`cross_language_gold_standard_v1.jsonl` records the expected evidence paths.
Run it after building the local corpus and embeddings:

```powershell
python tools/run_hybrid_retrieval.py `
  --chunks "rag/generated/aipm-wiki/chunks.jsonl" `
  --cases "rag/tests/cross_language_acceptance_cases_v1.jsonl" `
  --gold-standard "rag/tests/cross_language_gold_standard_v1.jsonl" `
  --model-cache "rag/models/bge-m3" `
  --embeddings "rag/generated/bge-m3/chunk_embeddings.npy" `
  --output "rag/generated/cross-language-v1/report.json" `
  --routing-config "rag/config/intent_routes_v1.json"
```

This checks retrieval only. A separate human review must verify that the Agent
answers in the user's language while preserving the original Chinese source
title and URL.

These cases are the Agent's product-level retrieval checks. They are not model
benchmarks and do not prescribe wording for the final answer. A case passes when the
retrieval layer returns useful, correctly scoped evidence for the orchestrator.

## How to evaluate a case

1. Apply `expected_stage_filters` before retrieval.
2. Run keyword and semantic retrieval over the same filtered corpus.
3. Inspect the top five results. At least one result must match a listed
   `expected_path_hint` when `minimum_relevant_hits` is one or higher.
4. Check `required_response_behavior`; it is part of the Agent's behavior, even when
   the RAG retrieval itself is correct.
5. Record pass/fail, top results, and the failure reason. Do not silently change a
   test after a poor result; add a versioned follow-up case instead.

The `P0` cases include the PRD's ten preset learning scenarios and the minimum
career/route/resource coverage needed for the MVP. `P1` cases probe edge conditions
such as current information and dated community interview signals.

## Gold-standard evidence

`gold_standard_v1.jsonl` records the evidence judgment for each test: primary
documents, acceptable alternatives, and the answer evidence that must be present.
The initial `expected_path_hints` remain useful as automated checks, but are not the
only documents that can support a correct answer. Semantic retrieval should be judged
against this wider evidence set and then sampled by a human reviewer.
