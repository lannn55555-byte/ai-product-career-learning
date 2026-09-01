# Agent RAG corpus pipeline

This folder contains the reproducible ingestion pipeline for the Agent's long-lived
domain corpus. The generated corpus is deliberately local-only because it contains
third-party source text. The source repository remains the source of truth.

## Inputs and outputs

Input: either the optional local `archlizheng/AIPM-Wiki` default source or a
folder of user-authorized AI PM documents.

Outputs under an ignored `rag/generated/<knowledge-base-id>/` directory:

- `source_manifest.jsonl`: one record per source Markdown document, with routing,
  freshness, and provenance metadata.
- `chunks.jsonl`: retrieval units produced from the source documents. These are the
  only records that later receive embeddings.
- `build_report.json`: reproducibility and quality-check summary.

## First-pass chunking rules

1. Treat Markdown heading boundaries as semantic boundaries. Preserve the document
   title and full heading path on every chunk.
2. Keep a complete interview question or a small section together. Long sections
   split at paragraph/block boundaries, not arbitrary character positions.
3. Target 300–700 Chinese characters of body text. Split only above 900 characters;
   merge a short trailing fragment below 150 characters with its preceding sibling.
4. Keep fenced code blocks, tables, and lists intact. Add a small paragraph overlap
   only when one long section needs multiple chunks.
5. Index `README.md` as low-priority navigation content rather than discard it.

The first pipeline is deterministic. Do not add embeddings, a vector database, or an
Agent framework until sampled chunks and retrieval acceptance cases are approved.

### Link handling

Each chunk preserves its original `text` for citation, plus an `outbound_references`
array for internal Markdown links. Link-only navigation phrases such as `详见 [xxx]`
are removed only from `retrieval_text`, because they are evidence that another
document may help, not evidence that this chunk answers the question. In a later
second-hop fallback, the retriever may use `outbound_references` to expand a weak
first-pass result.

## Keyword baseline

Before adding embeddings, run the dependency-free BM25-style lexical baseline against
the acceptance set. It uses Chinese character bigrams and English tokens, applies the
Agent's stage filter first, and writes inspectable Top-5 results.

```powershell
python tools/run_keyword_retrieval_baseline.py `
  --chunks "rag/generated/aipm-wiki/chunks.jsonl" `
  --cases "rag/tests/retrieval_acceptance_cases.jsonl" `
  --gold-standard "rag/tests/gold_standard_v1.jsonl" `
  --output "rag/generated/keyword-baseline/report.json"
```

This is a baseline, not the production retriever. Review failed cases before deciding
whether the fault lies in metadata, chunking, vocabulary, or the need for semantic
retrieval. The report keeps the original strict path result and also reports recall
against the gold standard's primary and acceptable alternative evidence.

## Local semantic-retrieval evaluation

`BAAI/bge-m3` is the current free local model for the first semantic-retrieval
experiment. It has already been downloaded under `rag/models/bge-m3/`. The command
below makes no network request: `local_files_only=True` is enforced by the script.
It stores an embedding matrix and report under the ignored `rag/generated/` folder.

```powershell
.\rag\.venv-embed\Scripts\python.exe tools/run_local_embedding_retrieval.py `
  --chunks "rag/generated/aipm-wiki/chunks.jsonl" `
  --cases "rag/tests/retrieval_acceptance_cases.jsonl" `
  --gold-standard "rag/tests/gold_standard_v1.jsonl" `
  --model-cache "rag/models/bge-m3" `
  --embeddings-output "rag/generated/bge-m3/chunk_embeddings.npy" `
  --output "rag/generated/bge-m3/report.json" `
  --top-k 5 `
  --batch-size 8
```

The first run creates 1,498 local vectors and can take several minutes on CPU. For
subsequent retrieval-only checks, add `--reuse-embeddings`; the script will reuse
the saved matrix only if its number of rows still matches the current corpus.

Compare these fields in the semantic and keyword reports:

- `gold_primary_recall_rate`: whether the best pre-audited evidence source appears
  in Top-K. This is the main quality signal for this small acceptance set.
- `gold_evidence_recall_rate`: whether either a primary source or an approved
  alternative appears in Top-K.
- `pass_rate`: the older, intentionally strict expected-path check; retain it as a
  diagnostic but do not treat it as the sole quality verdict.

If dense retrieval is not clearly better for an intent, the production design keeps
both approaches: lexical Top-20 + dense Top-20, deduplicate, rerank, then send only
3–5 cited chunks to the answer model.

## Hybrid retrieval V1

The first hybrid experiment does not add a reranker. It uses Reciprocal Rank Fusion
(RRF): a chunk gains a small score from its position in the lexical list and another
from its position in the dense list. A chunk found by both methods therefore rises
above one found weakly by only one. `README.md` navigation pages retain eligibility
but receive a small documented penalty, because they list many topics without usually
providing answer-level evidence.

```powershell
.\rag\.venv-embed\Scripts\python.exe tools/run_hybrid_retrieval.py `
  --chunks "rag/generated/aipm-wiki/chunks.jsonl" `
  --cases "rag/tests/retrieval_acceptance_cases.jsonl" `
  --gold-standard "rag/tests/gold_standard_v1.jsonl" `
  --model-cache "rag/models/bge-m3" `
  --embeddings "rag/generated/bge-m3/chunk_embeddings.npy" `
  --output "rag/generated/hybrid-v1/report.json" `
  --keyword-top-k 20 `
  --dense-top-k 20 `
  --final-top-k 5
```

Compare this report with the two baseline reports before adding a reranker. Add a
reranker only when Hybrid V1 still returns topical-but-not-answering chunks in its
final Top-5; it should rerank the hybrid candidate pool rather than scan the entire
corpus.

## Runtime evidence tool

The current Agent-facing interface is the local MCP server at
`mcp_server/aipm_retrieval_server.py`. It exposes
`retrieve_aipm_evidence` as a model-callable tool. Setup and the tool boundary
are documented in `docs/codex-native-agent-setup.md`; the Agent's evidence rules
are in `AGENTS.md` and `rag/config/agent_retrieval_policy_v1.md`.

### Initialize local evidence

The obsolete one-shot CLI evidence script is not distributed. Use the MCP server
for Agent calls. Before starting the server, initialize one local knowledge base
from the repository root:

```powershell
python -m pip install -r requirements-rag.txt
python tools/setup_codex_rag.py --default-aipm --accept-aipm-license
```

To use documents you are authorized to process instead of the default source:

```powershell
python tools/setup_codex_rag.py `
  --custom-source "C:\path\to\my-ai-pm-documents" `
  --source-name "My AI PM notes" `
  --source-id my-ai-pm-notes `
  --confirm-rights
```

The setup command stores only the active knowledge-base configuration locally.
Source text, chunks, embeddings, and model files remain ignored. See
`docs/codex-native-agent-setup.md` and `THIRD_PARTY_NOTICES.md` for the MCP
configuration and source-license boundary.

The Agent's use / no-use / web-verification rules are in
`rag/config/agent_retrieval_policy_v1.md`.

The final evidence set applies document-aware diversification only after retrieval:
all chunks remain eligible in the lexical and dense Top-20 pools, while the final
3–5 evidence set normally permits at most two chunks from the same document. When a
second chunk is used, an adjacent chunk is preferred to preserve a continuous
argument. Set `--max-chunks-per-document 0` only for diagnostic comparison runs.

### Routing and fusion experiments

Hybrid V2 adds two deliberately constrained controls. Both are visible in every
result row, so they can be reviewed rather than silently steering answers.

- Intent routing detects a small set of user intents (learning plan, portfolio,
  interview, career direction, troubleshooting, concept explanation). It applies
  tiny boosts only within the case's existing stage-filtered candidate pool. It
  cannot add a source that retrieval did not find.
- Fusion weights let evaluation test whether an intent benefits more from lexical
  precision or dense semantic recall. Do not tune only for the 20 current cases:
  retain unseen user questions as a later holdout set.

```powershell
.\rag\.venv-embed\Scripts\python.exe tools/run_hybrid_retrieval.py `
  --chunks "rag/generated/aipm-wiki/chunks.jsonl" `
  --cases "rag/tests/retrieval_acceptance_cases.jsonl" `
  --gold-standard "rag/tests/gold_standard_v1.jsonl" `
  --model-cache "rag/models/bge-m3" `
  --embeddings "rag/generated/bge-m3/chunk_embeddings.npy" `
  --output "rag/generated/hybrid-v2/report.json" `
  --routing-config "rag/config/intent_routes_v1.json" `
  --lexical-weight 1.0 `
  --dense-weight 1.0
```

## Rebuild and evaluate

Run `tools/setup_codex_rag.py` again whenever the selected local source is
changed. The command rebuilds the local corpus and embeddings before selecting it
for the MCP server. Use the evaluation runners above after that rebuild.

## What the Agent will filter on

`stage`, `content_type`, `freshness`, `source_class`, and `source_path` let the
orchestrator retrieve from the right part of the corpus before hybrid search. Dynamic
provider facts are never treated as current merely because they occur in this corpus;
they require an official-source verification at response time.
