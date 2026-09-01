#!/usr/bin/env python3
"""Build a local RAG corpus from user-authorized Markdown, TXT, PDF, or DOCX files."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_aipm_wiki_corpus import (  # noqa: E402
    Section,
    chunk_section,
    document_title,
    jsonl_write,
    normalize_text,
    record_id,
    retrieval_body,
)


SUPPORTED_SUFFIXES = {".md", ".txt", ".pdf", ".docx"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--source-name", required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--source-url")
    parser.add_argument("--source-license", default="user-provided")
    parser.add_argument("--stage", default="learning")
    return parser.parse_args()


def read_text(path: Path) -> str:
    if path.suffix.lower() in {".md", ".txt"}:
        return path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as error:
            raise SystemExit("PDF import requires pip install -r requirements-rag.txt.") from error
        return "\n\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
    if path.suffix.lower() == ".docx":
        try:
            from docx import Document
        except ImportError as error:
            raise SystemExit("DOCX import requires pip install -r requirements-rag.txt.") from error
        return "\n".join(paragraph.text for paragraph in Document(path).paragraphs)
    raise ValueError(f"Unsupported file: {path}")


def main() -> None:
    args = parse_args()
    if not args.source_id.replace("-", "").replace("_", "").isalnum():
        raise SystemExit("--source-id may contain only letters, digits, hyphens, and underscores.")
    source_root = args.source_root.resolve()
    output_root = args.output_root.resolve()
    if not source_root.is_dir():
        raise SystemExit(f"Source directory does not exist: {source_root}")
    files = [path for path in sorted(source_root.rglob("*")) if path.suffix.lower() in SUPPORTED_SUFFIXES]
    if not files:
        raise SystemExit("No supported Markdown, TXT, PDF, or DOCX files were found.")

    output_root.mkdir(parents=True, exist_ok=True)
    verified_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    manifests: list[dict] = []
    chunks: list[dict] = []
    for source_file in files:
        relative = source_file.relative_to(source_root)
        text = normalize_text(read_text(source_file))
        if not text:
            continue
        title = document_title(text, source_file.stem)
        source_path = relative.as_posix()
        source_url = args.source_url or f"local://{args.source_id}/{source_path}"
        document_id = record_id("doc", args.source_id, source_path)
        manifests.append({
            "document_id": document_id, "source_id": args.source_id, "source_repository": args.source_url,
            "source_url": source_url, "source_path": source_path, "title": title, "stage": args.stage,
            "content_type": "user_document", "freshness": "user_managed", "source_class": "learner_provided",
            "license": args.source_license, "source_commit": None, "verified_at": verified_at,
            "character_count": len(text),
        })
        position = 0
        for sequence, body in enumerate(chunk_section(Section([title], text)), start=1):
            position += 1
            retrieval_text, removed = retrieval_body(body)
            chunks.append({
                "chunk_id": record_id("chunk", document_id, str(sequence), body),
                "document_id": document_id, "document_chunk_position": position, "source_id": args.source_id,
                "source_url": source_url, "source_path": source_path, "title": title,
                "heading_path": [title], "stage": args.stage, "content_type": "user_document",
                "freshness": "user_managed", "source_class": "learner_provided",
                "license": args.source_license, "source_commit": None, "verified_at": verified_at,
                "text": body, "outbound_references": [],
                "navigation_lines_removed_from_retrieval": removed,
                "retrieval_text": f"标题：{title}\n路径：{title}\n\n{retrieval_text}",
                "character_count": len(body), "embedding": None,
            })
    if not chunks:
        raise SystemExit("No extractable text was found in the supported files.")
    jsonl_write(output_root / "source_manifest.jsonl", manifests)
    jsonl_write(output_root / "chunks.jsonl", chunks)
    report = {"source_id": args.source_id, "source_name": args.source_name, "source_url": args.source_url,
              "source_license": args.source_license, "verified_at": verified_at,
              "documents": len(manifests), "chunks": len(chunks), "stage": args.stage}
    (output_root / "build_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
