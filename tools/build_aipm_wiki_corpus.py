#!/usr/bin/env python3
"""Build a local, auditable RAG corpus from archlizheng/AIPM-Wiki Markdown.

The script intentionally creates chunks only. Embeddings are a later, separate
operation so that chunk quality can be checked before any provider or vector-store
choice is made.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable


SOURCE_REPOSITORY = "https://github.com/archlizheng/AIPM-Wiki"
SOURCE_ID = "aipm-wiki"
MIN_CHARS = 150
TARGET_CHARS = 700
MAX_CHARS = 900
OVERLAP_CHARS = 120

STAGE_RULES = {
    "00-roadmap": ("diagnosis", "career_framework", "stable"),
    "01-ai-basics": ("learning", "concept", "stable"),
    "02-pm-skills": ("application", "framework", "stable"),
    "03-case-studies": ("case", "case_study", "dated_reference"),
    "04-interview": ("interview", "interview_question", "dated_signal"),
    "05-resources": ("resources", "resource_index", "dated_reference"),
}


@dataclass(frozen=True)
class Section:
    heading_path: list[str]
    text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    return parser.parse_args()


def git_commit(source_root: Path) -> str | None:
    try:
        return subprocess.check_output(
            [
                "git",
                "-c",
                f"safe.directory={source_root.as_posix()}",
                "-C",
                str(source_root),
                "rev-parse",
                "HEAD",
            ],
            text=True,
            encoding="utf-8",
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
NAVIGATION_CUE = re.compile(r"(?:详见|参见|查看|延伸阅读|相关阅读|相关资料|可参考|概念铺垫见|更多资料)")


def outbound_references(text: str, source_path: str) -> list[dict]:
    """Extract internal Markdown links as provenance, not as answer evidence."""
    references: list[dict] = []
    seen: set[tuple[str, str, str | None]] = set()
    parent = posixpath.dirname(source_path)
    for label, raw_target in MARKDOWN_LINK.findall(text):
        target = raw_target.strip().strip("<>")
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target_path, separator, anchor = target.partition("#")
        target_path = target_path.split(maxsplit=1)[0]
        resolved = posixpath.normpath(posixpath.join(parent, target_path))
        if not resolved.startswith("docs/") or not resolved.endswith(".md"):
            continue
        key = (label.strip(), resolved, anchor if separator else None)
        if key in seen:
            continue
        seen.add(key)
        references.append(
            {
                "label": label.strip(),
                "resolved_source_path": resolved,
                "anchor": anchor if separator else None,
            }
        )
    return references


def retrieval_body(text: str) -> tuple[str, int]:
    """Keep substantive text while removing link-only navigation statements.

    The original chunk text is preserved for citation and display. Only the text
    used for lexical and embedding retrieval is weakened, so a phrase such as
    '详见 [xxx](...)' does not make its source rank as if it explained xxx.
    """
    kept: list[str] = []
    removed = 0
    for line in text.splitlines():
        if MARKDOWN_LINK.search(line) and NAVIGATION_CUE.search(line):
            removed += 1
            continue
        kept.append(line)
    return normalize_text("\n".join(kept)), removed


def document_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return fallback.replace("-", " ").title()


def sections_from_markdown(text: str, title: str) -> list[Section]:
    """Split at H2/H3 boundaries while retaining title and ancestor headings."""
    headings: dict[int, str] = {1: title}
    sections: list[Section] = []
    buffer: list[str] = []
    current_path = [title]

    def flush() -> None:
        body = normalize_text("\n".join(buffer))
        if body:
            sections.append(Section(current_path.copy(), body))
        buffer.clear()

    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not match:
            buffer.append(line)
            continue

        level = len(match.group(1))
        heading = match.group(2).strip()
        if level == 1:
            headings[1] = heading
            current_path = [heading]
            continue

        if level <= 3:
            flush()
            headings[level] = heading
            for deeper in tuple(headings):
                if deeper > level:
                    del headings[deeper]
            current_path = [headings[key] for key in sorted(headings) if key <= level]
        else:
            buffer.append(line)

    flush()
    return sections or [Section([title], normalize_text(text))]


def blocks(text: str) -> list[str]:
    """Create non-breakable paragraph/list/table/code blocks for a section."""
    result: list[str] = []
    current: list[str] = []
    in_fence = False

    def flush() -> None:
        value = normalize_text("\n".join(current))
        if value:
            result.append(value)
        current.clear()

    for line in text.splitlines():
        if line.strip().startswith("```"):
            current.append(line)
            in_fence = not in_fence
            if not in_fence:
                flush()
            continue
        if in_fence:
            current.append(line)
            continue
        if not line.strip():
            flush()
            continue
        current.append(line)
    flush()
    return result


def tail_overlap(text: str) -> str:
    """Return only complete final sentences; never cut Markdown in the middle."""
    sentences = re.findall(r"[^。！？!?]*[。！？!?]", text)
    selected: list[str] = []
    length = 0
    for sentence in reversed(sentences):
        if length + len(sentence) > OVERLAP_CHARS:
            break
        selected.append(sentence)
        length += len(sentence)
    return "".join(reversed(selected)).strip()


def chunk_section(section: Section) -> list[str]:
    """Split a long section at block boundaries, retaining useful local overlap."""
    section_blocks = blocks(section.text)
    if not section_blocks:
        return []

    chunks: list[str] = []
    current = ""
    previous = ""
    for block in section_blocks:
        separator = "\n\n" if current else ""
        proposed = f"{current}{separator}{block}"
        if current and len(proposed) > MAX_CHARS:
            chunks.append(current)
            overlap = tail_overlap(previous or current)
            current = f"{overlap}\n\n{block}" if overlap else block
        else:
            current = proposed
        previous = current
    if current:
        chunks.append(current)

    if len(chunks) > 1 and len(chunks[-1]) < MIN_CHARS:
        chunks[-2] = f"{chunks[-2]}\n\n{chunks[-1]}"
        chunks.pop()
    return chunks


def classify(relative_path: Path) -> tuple[str, str, str]:
    top_level = relative_path.parts[1]
    stage, content_type, freshness = STAGE_RULES[top_level]
    parts = set(relative_path.parts)
    if relative_path.name.lower() == "readme.md":
        content_type = "navigation"
    elif top_level == "04-interview" and "experiences" in parts:
        content_type, freshness = "interview_experience", "dated_signal"
    elif top_level == "05-resources":
        content_type = "resource_index"
    elif "model-landscape" in relative_path.name or "tool-landscape" in relative_path.name:
        freshness = "dynamic_reference"
    return stage, content_type, freshness


def record_id(prefix: str, *values: str) -> str:
    digest = hashlib.sha1("\0".join(values).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"


def jsonl_write(path: Path, records: Iterable[dict]) -> int:
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    return count


def main() -> None:
    args = parse_args()
    source_root = args.source_root.resolve()
    docs_root = source_root / "docs"
    output_root = args.output_root.resolve()
    if not docs_root.is_dir():
        raise SystemExit(f"No docs directory at {docs_root}")

    output_root.mkdir(parents=True, exist_ok=True)
    source_files = sorted(docs_root.rglob("*.md"))
    verified_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    commit = git_commit(source_root)
    manifests: list[dict] = []
    chunks: list[dict] = []
    stage_counts: dict[str, int] = {}

    for source_file in source_files:
        relative = source_file.relative_to(source_root)
        text = normalize_text(source_file.read_text(encoding="utf-8"))
        title = document_title(text, source_file.stem)
        stage, content_type, freshness = classify(relative)
        document_id = record_id("doc", str(relative))
        source_url = f"{SOURCE_REPOSITORY}/blob/{commit or 'main'}/{relative.as_posix()}"
        manifest = {
            "document_id": document_id,
            "source_id": SOURCE_ID,
            "source_repository": SOURCE_REPOSITORY,
            "source_url": source_url,
            "source_path": relative.as_posix(),
            "title": title,
            "stage": stage,
            "content_type": content_type,
            "freshness": freshness,
            "source_class": "community",
            "license": "CC-BY-NC-SA-4.0",
            "source_commit": commit,
            "verified_at": verified_at,
            "character_count": len(text),
        }
        manifests.append(manifest)
        stage_counts[stage] = stage_counts.get(stage, 0) + 1

        # An interview document is normally one complete prompt, answer, and follow-up
        # set. Splitting each H2 (for example, "考察点" and "参考答案") creates tiny,
        # contextless retrieval units, so retain the full question document first.
        if stage == "interview" and content_type != "navigation":
            document_sections = [Section([title], text)]
        else:
            document_sections = sections_from_markdown(text, title)

        document_chunk_position = 0
        for section in document_sections:
            for sequence, body in enumerate(chunk_section(section), start=1):
                document_chunk_position += 1
                clean_body, navigation_lines_removed = retrieval_body(body)
                references = outbound_references(body, relative.as_posix())
                chunk_id = record_id("chunk", document_id, " > ".join(section.heading_path), str(sequence), body)
                chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "document_id": document_id,
                        "document_chunk_position": document_chunk_position,
                        "source_id": SOURCE_ID,
                        "source_url": source_url,
                        "source_path": relative.as_posix(),
                        "title": title,
                        "heading_path": section.heading_path,
                        "stage": stage,
                        "content_type": content_type,
                        "freshness": freshness,
                        "source_class": "community",
                        "license": "CC-BY-NC-SA-4.0",
                        "source_commit": commit,
                        "verified_at": verified_at,
                        "text": body,
                        "outbound_references": references,
                        "navigation_lines_removed_from_retrieval": navigation_lines_removed,
                        "retrieval_text": (
                            f"标题：{title}\n"
                            f"路径：{' > '.join(section.heading_path)}\n\n"
                            f"{clean_body}"
                        ),
                        "character_count": len(body),
                        "embedding": None,
                    }
                )

    manifest_count = jsonl_write(output_root / "source_manifest.jsonl", manifests)
    chunk_count = jsonl_write(output_root / "chunks.jsonl", chunks)
    report = {
        "source_id": SOURCE_ID,
        "source_repository": SOURCE_REPOSITORY,
        "source_commit": commit,
        "verified_at": verified_at,
        "documents": manifest_count,
        "chunks": chunk_count,
        "stages": stage_counts,
        "chunking": {
            "min_chars": MIN_CHARS,
            "target_chars": TARGET_CHARS,
            "max_chars": MAX_CHARS,
            "overlap_chars": OVERLAP_CHARS,
        },
    }
    (output_root / "build_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
