# MCP Client Configs

Use this file when you need concrete client wiring examples for `adk-agent-extension`.

## Shared Server Definition

All clients should map to the same stdio process:

- command: `node`
- args: `["/absolute/path/to/adk-agent-extension/dist/google-adk-agent-extension.js"]`

Build first when running from source:

```bash
bun install
bun run build
```

## Codex / Claude Code / Cline / Cursor

Use each client's MCP settings UI/file and add a stdio server entry with:

```json
{
  "name": "adk-agent-extension",
  "command": "node",
  "args": ["/absolute/path/to/adk-agent-extension/dist/google-adk-agent-extension.js"]
}
```

Notes:
- Some clients use `mcpServers` object shape; others use an array.
- Keep the same `command`/`args` values regardless of shape.
- Reload the client after saving settings.

## Gemini CLI (Extension Shortcut)

Gemini can install the extension directly, which auto-registers the bundled MCP server:

```bash
gemini extensions install https://github.com/simonliu-ai-product/adk-agent-extension
```

For local development:

```bash
gemini extensions install .
```

## Verification Steps

1. Open MCP tool list in the client.
2. Confirm tools like `list_adks` and `list_adk_agents` are present.
3. Call `list_adks`.
4. If empty or failing, check `adk_agent_list.json` and ADK server URLs.
