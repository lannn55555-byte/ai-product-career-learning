#!/usr/bin/env python3
"""Initialize the default AIPM knowledge base or a user-authorized AI PM source."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AIPM_REPO = "https://github.com/archlizheng/AIPM-Wiki.git"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--default-aipm", action="store_true")
    mode.add_argument("--custom-source", type=Path)
    parser.add_argument("--accept-aipm-license", action="store_true")
    parser.add_argument("--confirm-rights", action="store_true")
    parser.add_argument("--source-name")
    parser.add_argument("--source-id")
    parser.add_argument("--source-url")
    parser.add_argument("--source-license", default="user-provided")
    parser.add_argument("--stage", default="learning")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--batch-size", type=int, default=8)
    return parser.parse_args()


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def clone_default_source() -> Path:
    destination = PROJECT_ROOT / "rag" / "sources" / "AIPM-Wiki"
    if destination.is_dir():
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "clone", "--depth", "1", DEFAULT_AIPM_REPO, str(destination)])
    return destination


def relative(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def write_active_config(name: str, corpus_root: Path) -> None:
    config = {
        "schema_version": 1,
        "name": name,
        "chunks_path": relative(corpus_root / "chunks.jsonl"),
        "embeddings_path": relative(corpus_root / "chunk_embeddings.npy"),
        "model_cache": "rag/models/bge-m3",
        "routing_config": "rag/config/intent_routes_v1.json",
    }
    destination = PROJECT_ROOT / "rag" / "local" / "active_knowledge_base.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    python = sys.executable
    if args.default_aipm:
        if not args.accept_aipm_license:
            raise SystemExit(
                "Default AIPM setup requires --accept-aipm-license. "
                "AIPM-Wiki is CC BY-NC-SA 4.0: attribution, non-commercial use, and share-alike apply."
            )
        source_root = clone_default_source()
        corpus_root = PROJECT_ROOT / "rag" / "generated" / "aipm-wiki"
        run([python, str(PROJECT_ROOT / "tools" / "build_aipm_wiki_corpus.py"),
             "--source-root", str(source_root), "--output-root", str(corpus_root)])
        name = "AIPM Wiki default knowledge base"
    else:
        if not args.confirm_rights:
            raise SystemExit(
                "Custom setup requires --confirm-rights. Only import material you are authorized to process."
            )
        if not args.source_name or not args.source_id:
            raise SystemExit("Custom setup requires --source-name and --source-id.")
        source_root = args.custom_source.resolve()
        corpus_root = PROJECT_ROOT / "rag" / "generated" / f"custom-{args.source_id}"
        run([python, str(PROJECT_ROOT / "tools" / "build_local_corpus.py"),
             "--source-root", str(source_root), "--output-root", str(corpus_root),
             "--source-name", args.source_name, "--source-id", args.source_id,
             "--source-license", args.source_license, "--stage", args.stage]
            + (["--source-url", args.source_url] if args.source_url else []))
        name = args.source_name

    run([python, str(PROJECT_ROOT / "tools" / "build_embeddings.py"),
         "--chunks", str(corpus_root / "chunks.jsonl"),
         "--embeddings-output", str(corpus_root / "chunk_embeddings.npy"),
         "--model-cache", str(PROJECT_ROOT / "rag" / "models" / "bge-m3"),
         "--device", args.device, "--batch-size", str(args.batch_size)])
    write_active_config(name, corpus_root)
    print(f"Knowledge base ready: {name}")
    print("Restart Codex or start a new task before using the MCP retrieval tool.")


if __name__ == "__main__":
    main()
