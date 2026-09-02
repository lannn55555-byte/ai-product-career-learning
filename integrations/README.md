# Other Agent hosts

The learning method, state files, local corpus builder, embeddings, and MCP
retrieval server are shared core components. This repository includes host
adapters for Codex, Claude Code, Cursor, and Antigravity.

All hosts need a local checkout of this repository, a Python environment with
`requirements-rag.txt` installed, and an initialized knowledge base. Do not
commit `rag/generated/`, `rag/sources/`, `rag/models/`, `rag/local/`, or learner
state to a public repository.

## Shared local knowledge-base setup

Run one of these from the repository root after reviewing the applicable
rights/notice. These commands build chunks and embeddings locally and select
one active knowledge base; they do not register any Codex-specific tool.

~~~powershell
python -m pip install -r requirements-rag.txt
python tools/setup_knowledge_base.py --default-aipm --accept-aipm-license
~~~

For user-authorized files in one local folder:

~~~powershell
python tools/setup_knowledge_base.py `
  --custom-source "C:\path\to\my-ai-pm-documents" `
  --source-name "My AI PM notes" `
  --source-id my-ai-pm-notes `
  --confirm-rights
~~~

Supported files are Markdown, TXT, PDF, and DOCX. The selected custom folder
becomes the active library; this V1 does not merge it with AIPM-Wiki or watch
for later file changes.

## Claude Code

This repository includes a project-scoped `.mcp.json` and a router Skill at
`.claude/skills/ai-product-career-learning/SKILL.md`. Open the repository with
Claude Code, approve the project MCP server when Claude Code asks, then use
normal language such as “Here is my resume; help me transition to AI product.”

The router loads the canonical `AGENTS.md` and the matching Skill under
`skills/`, so it can use the same state and evidence rules as Codex. The
`.mcp.json` uses `${PYTHON:-python}`; set `PYTHON` to the Python executable
where you installed `requirements-rag.txt` if `python` is not the right one.

Claude Desktop's local MCP connection can expose the retrieval tool, but the
full stateful workflow needs a local workspace-capable host such as Claude
Code. Claude's cloud connectors and Cowork do not use a local
`claude_desktop_config.json` server.

## Cursor

This repository includes `.cursor/mcp.json` and an always-applied project rule
at `.cursor/rules/ai-product-career-learning.mdc`. Open the repository as a
Cursor workspace, select the MCP server under **Customize**, and approve its
use when Cursor asks.

Cursor resolves `${workspaceFolder}` in the checked-in MCP configuration. Make
sure its `python` command is the environment where the RAG dependencies were
installed; otherwise change only the local configuration to that executable.

## Antigravity

This repository includes the workspace MCP configuration at
`.agents/mcp_config.json` and the workflow rule at
`.agents/rules/ai-product-career-learning.md`. Open the repository as an
Antigravity workspace and mark the rule **Always On** in the Rules panel if the
host has not already done so. Approve the MCP tool on first use.

The configuration assumes `python` resolves to the environment where the RAG
dependencies were installed and uses the workspace root as its working
directory. If your environment differs, edit the local `command` or `cwd`
values rather than committing a personal absolute path.

## Behaviour contract

These adapters share the same business behaviour, but not identical UI:

- natural-language diagnosis, planning, learning, state, and retrieval policy;
- explicit permission before accepting third-party source terms or processing
  user files;
- local source data and learner state stay in ignored folders; and
- a new host task/session may be needed after building or switching a knowledge
  base so its MCP process loads the current configuration.

Do not claim that every host has Codex's approval UI or automatic Skill routing.
