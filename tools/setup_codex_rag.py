#!/usr/bin/env python3
"""Build a local knowledge base and register its MCP server with Codex."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SERVER_NAME = "aipm_local_evidence"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--default-aipm", action="store_true")
    source.add_argument("--custom-source", type=Path)
    parser.add_argument("--accept-aipm-license", action="store_true")
    parser.add_argument("--confirm-rights", action="store_true")
    parser.add_argument("--source-name")
    parser.add_argument("--source-id")
    parser.add_argument("--source-url")
    parser.add_argument("--source-license", default="user-provided")
    parser.add_argument("--stage", default="learning")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--server-name", default=DEFAULT_SERVER_NAME)
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="Replace an MCP server with the same name in the local Codex configuration.",
    )
    return parser.parse_args()


def knowledge_base_command(args: argparse.Namespace, python: str) -> list[str]:
    command = [python, str(PROJECT_ROOT / "tools" / "setup_knowledge_base.py")]
    if args.default_aipm:
        if not args.accept_aipm_license:
            raise SystemExit(
                "Default AIPM setup requires --accept-aipm-license. "
                "Read THIRD_PARTY_NOTICES.md before accepting."
            )
        return command + ["--default-aipm", "--accept-aipm-license", "--device", args.device,
                          "--batch-size", str(args.batch_size)]
    if not args.confirm_rights:
        raise SystemExit("Custom setup requires --confirm-rights.")
    if not args.source_name or not args.source_id:
        raise SystemExit("Custom setup requires --source-name and --source-id.")
    command += [
        "--custom-source", str(args.custom_source),
        "--confirm-rights",
        "--source-name", args.source_name,
        "--source-id", args.source_id,
        "--source-license", args.source_license,
        "--stage", args.stage,
        "--device", args.device,
        "--batch-size", str(args.batch_size),
    ]
    if args.source_url:
        command += ["--source-url", args.source_url]
    return command


def mcp_add_command(server_name: str, python: str) -> list[str]:
    return [
        "codex", "mcp", "add", server_name, "--", python,
        str(PROJECT_ROOT / "mcp_server" / "aipm_retrieval_server.py"),
    ]


def mcp_server_exists(server_name: str) -> bool:
    result = subprocess.run(
        ["codex", "mcp", "get", server_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def main() -> None:
    args = parse_args()
    if shutil.which("codex") is None:
        raise SystemExit("Codex CLI was not found. Install or start Codex before registering this MCP server.")
    python = sys.executable
    existing_server = mcp_server_exists(args.server_name)
    if existing_server and not args.replace_existing:
        raise SystemExit(
            f"Codex already has an MCP server named '{args.server_name}'. "
            "Use --replace-existing only if you want this project to replace it."
        )
    run(knowledge_base_command(args, python))
    if existing_server:
        run(["codex", "mcp", "remove", args.server_name])
    run(mcp_add_command(args.server_name, python))
    print("Local knowledge base initialized and MCP server registered.")
    print("Start a new Codex task before asking a source-backed question.")


if __name__ == "__main__":
    main()
