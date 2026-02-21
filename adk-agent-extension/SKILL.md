---
name: adk-agent-extension
description: Use this skill when the user wants any MCP-capable agent or IDE assistant to interact with Google ADK agents through the adk-agent-extension MCP server. Trigger for requests like wiring ADK tools into Codex/Claude Code/Cursor/Cline/Gemini, registering a stdio MCP server, listing ADK servers/agents, creating sessions, and chatting with ADK agents.
---

# ADK Agent Extension

## Overview

Use `adk-agent-extension` as an MCP server that any MCP-capable agent client can connect to.

Use this for:
- ADK discovery (`list_adks`, `list_adk_agents`)
- ADK chat/session flow (`create_session`, `send_message_to_agent`, streaming/session helpers)
- ADK helper operations (create/deploy/evaluate/list tools/safety/visualize)

## Workflow

1. Build artifacts locally when needed:
```bash
bun install
bun run build
```
2. Register MCP stdio server in the target client:
   - command: `node`
   - args: `["/absolute/path/to/adk-agent-extension/dist/google-adk-agent-extension.js"]`
3. Reopen/reload the client and verify tools are visible.
4. Run ADK flow:
   - `list_adks`
   - `list_adk_agents`
   - `create_session`
   - `send_message_to_agent`

Use client-specific config examples from `references/client-configs.md`.

## Gemini CLI Setup (Optional Client-Specific Shortcut)

For Gemini CLI users, install directly:
```bash
gemini extensions install https://github.com/simonliu-ai-product/adk-agent-extension
```

## Bundled MCP Server

The repo already defines MCP server wiring:
- File: `gemini-extension.json`
- Key: `mcpServers.nodeServer`
- Command: `node`
- Entrypoint: `${extensionPath}/dist/google-adk-agent-extension.js`

Implication:
- In Gemini CLI extension mode, MCP registration is automatic on install.
- In other clients, manually register equivalent stdio config.

## Portable Tool Surface (All MCP Clients)

- `list_adks`
- `list_adk_agents`
- `create_session`
- `send_message_to_agent`
- `stream_message_to_agent`
- `manage_chat_session`
- `create_agent`
- `deploy_agent`
- `evaluate_agent`
- `list_agent_tools`
- `scan_agent_safety`
- `visualize_agent_system`

## Gemini-Only Slash Commands

- `/adk-ext:list_adks`
- `/adk-ext:list_adk_agent`
- `/adk-ext:agent_chat`
- `/adk-ext:interactive_chat`
- `/adk-ext:config_add_server`
- `/adk-ext:config_list_servers`
- `/adk-ext:config_remove_server`
- `/adk-ext:create_agent`
- `/adk-ext:deploy_agent`
- `/adk-ext:evaluate_agent`
- `/adk-ext:list_agent_tools`
- `/adk-ext:scan_safety`
- `/adk-ext:visualize`

## Configuration

Manage ADK server endpoints through `adk_agent_list.json` (extension root) or the config commands above.

Example:
```json
{
  "agents": [
    { "name": "my-adk-server", "url": "https://my-adk-server.example.com" }
  ]
}
```

## Troubleshooting

- If tools are missing, confirm your client is MCP-capable and loaded the stdio server config.
- If MCP calls fail, ensure `dist/google-adk-agent-extension.js` exists and `node` is available.
- If agent discovery fails, verify server URLs in `adk_agent_list.json`.
- If command names differ by client UI, call tools directly from MCP tool picker by exact tool name.

## Resources

### references/

- `references/client-configs.md`: quick MCP client configuration snippets for Codex, Claude Code, Cursor, Cline, and Gemini CLI.

### assets/

- `assets/mcp/adk-agent-extension.stdio.json`: reusable MCP stdio server template you can copy into client MCP settings.
