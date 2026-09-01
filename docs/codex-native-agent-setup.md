# Codex-native learning Agent setup

## What changes

Codex becomes the Agent runner. The local MCP server exposes one safe tool:
`retrieve_aipm_evidence`. The Codex model can decide whether to call it instead
of a Python script always retrieving before model generation.

## Tool boundary

- The tool only reads the checked-in local AIPM Wiki index.
- It returns evidence and source links, never conclusions about a user's past work.
- The model must ask for missing user experience instead of filling gaps from RAG.
- It must cite `title` and `source_url` whenever it relies on returned evidence.

## Codex configuration

Register this stdio server in the local Codex configuration:

```toml
[mcp_servers.aipm_local_evidence]
command = 'F:\\Work\\learning\\ai\\ai-product-career-learning\\rag\\.venv-embed\\Scripts\\python.exe'
args = ['F:\\Work\\learning\\ai\\ai-product-career-learning\\mcp_server\\aipm_retrieval_server.py']
startup_timeout_sec = 120
tool_timeout_sec = 120
```

Restart Codex or start a new local task after adding the server. Then ask a
source-backed question such as: "I have a UX background and 14 days to prepare
for AI product roles. What evidence should inform my learning priority?"

## What remains intentionally outside this MCP server

The existing Skills remain the business-method layer. The MCP server is only a
tool. Future work can package the Skills and this tool together as a Codex
plugin, but a plugin is not required to validate model-directed retrieval.
