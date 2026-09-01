# Codex-native learning Agent setup

## What changes

Codex is the Agent runner. The local MCP server exposes one safe tool,
retrieve_aipm_evidence. The Codex model decides when source-backed retrieval is
useful instead of always retrieving before a response.

## Initialize a local knowledge base

From the repository root, install the RAG dependencies in the same Python
environment that the MCP server will use:

~~~powershell
python -m pip install -r requirements-rag.txt
~~~

For the default AI PM learning library, run the setup command once. It clones
AIPM-Wiki locally, builds ignored chunks and embeddings, and records the active
local knowledge-base configuration:

~~~powershell
python tools/setup_knowledge_base.py --default-aipm --accept-aipm-license
~~~

The optional default source is governed by the third-party notice and its
CC BY-NC-SA 4.0 conditions. It is not included in this repository.

To build a local index from user-authorized AI PM documents instead, point the
same command at a folder of Markdown, TXT, PDF, or DOCX files:

~~~powershell
python tools/setup_knowledge_base.py --custom-source "C:\path\to\my-ai-pm-documents" --source-name "My AI PM notes" --source-id my-ai-pm-notes --confirm-rights
~~~

Custom documents remain local. The command replaces only the active local
knowledge base, not the checked-in Skills or learning rules.

## Tool boundary

- The tool only reads the currently initialized local knowledge base.
- It returns evidence and source links, never conclusions about a user's past work.
- The model must ask for missing user experience instead of filling gaps from RAG.
- It must cite title and source_url whenever it relies on returned evidence.

## Codex configuration

Register this stdio server in the local Codex configuration. Replace both
placeholder paths with your own Python executable and cloned repository path:

~~~toml
[mcp_servers.aipm_local_evidence]
command = 'C:\\path\\to\\python.exe'
args = ['C:\\path\\to\\ai-product-career-learning\\mcp_server\\aipm_retrieval_server.py']
startup_timeout_sec = 120
tool_timeout_sec = 120
~~~

Restart Codex or start a new local task after adding the server or switching
knowledge bases. Then ask a source-backed question such as: “I have a UX
background and 14 days to prepare for AI product roles. What evidence should
inform my learning priority?”

## What remains outside the MCP server

The Skills remain the business-method layer. The MCP server is only a tool.
Future work can package the Skills and this tool together as a Codex plugin,
but a plugin is not required to validate model-directed retrieval.
