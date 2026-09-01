#!/usr/bin/env python3
"""Create a local embedding matrix for a prepared RAG chunks.jsonl corpus."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from rag.local_retriever import DEFAULT_MODEL, load_jsonl


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunks", required=True, type=Path)
    parser.add_argument("--embeddings-output", required=True, type=Path)
    parser.add_argument("--model-cache", required=True, type=Path)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--batch-size", type=int, default=8)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    chunks = load_jsonl(args.chunks)
    if not chunks:
        raise SystemExit("The corpus is empty.")
    args.embeddings_output.parent.mkdir(parents=True, exist_ok=True)
    args.model_cache.mkdir(parents=True, exist_ok=True)
    model = SentenceTransformer(args.model, cache_folder=str(args.model_cache), device=args.device)
    texts = [chunk["retrieval_text"] for chunk in chunks]
    embeddings = model.encode(texts, batch_size=args.batch_size, convert_to_numpy=True, normalize_embeddings=True)
    np.save(args.embeddings_output, embeddings)
    fingerprint = hashlib.sha256("\n".join(chunk["chunk_id"] for chunk in chunks).encode("utf-8")).hexdigest()
    metadata = {"model": args.model, "chunks": len(chunks), "dimensions": int(embeddings.shape[1]),
                "corpus_fingerprint": fingerprint}
    args.embeddings_output.with_suffix(".metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
