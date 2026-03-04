---
name: openclaw-config
description: "Configure OpenClaw (AI chat gateway) on any OS, VM, or platform. Use when the user mentions openclaw, openclaw config, openclaw.json, openclaw setup, openclaw channels, openclaw gateway, openclaw sandbox, openclaw docker, openclaw install, or needs to create or edit an existing OpenClaw configuration. Handles fresh installs, editing existing configs, adding channels, models, providers, sandboxing, cron, hooks, sessions, and all gateway settings."
---

# OpenClaw Configuration

Configure OpenClaw on any OS, VM, or deployment target via natural language.

## First Step: Fetch Latest Docs Index

**Always** fetch the latest docs index before doing anything:

```bash
curl -fsSL https://docs.openclaw.ai/llms.txt
```

Use this index to find the right documentation page for the user's specific need, then fetch that page with `read_web_page` for up-to-date details.

## Overview

OpenClaw is an AI chat gateway that connects AI agents with chat apps (WhatsApp, Telegram, Discord, Slack, Signal, iMessage, etc.). Configuration lives at `~/.openclaw/openclaw.json` (JSON5 format -- comments and trailing commas allowed).

## Workflow

### 1. Determine User's Goal

Ask what they want:
- **Fresh install?** -> Guide through install + onboard + config
- **Edit existing config?** -> Read their current config first, then modify
- **Add a channel?** -> Add the channel block to their config
- **Change models/providers?** -> Update `agents.defaults.model` and `models.providers`
- **Set up sandboxing?** -> Configure `agents.defaults.sandbox`
- **Cron/automation?** -> Configure `cron`, `hooks`, or `automation`

### 2. Read Existing Config (if editing)

```bash
cat ~/.openclaw/openclaw.json 2>/dev/null || echo "No config found"
```

Also check:
```bash
openclaw doctor 2>/dev/null  # diagnose issues
openclaw status 2>/dev/null  # gateway status
```

### 3. Generate or Edit Config

- Config format: **JSON5** (comments + trailing commas OK)
- All fields optional -- OpenClaw uses safe defaults when omitted
- Config hot-reloads (no restart needed for most changes)
- Use `$include` to split config into multiple files

### 4. Validate

After writing config, run:
```bash
openclaw doctor
```

Fix any issues it reports. Use `openclaw doctor --fix` for auto-repair.

## Installation (any platform)

### macOS / Linux / WSL2
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### Windows (PowerShell)
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

### Docker
```bash
./docker-setup.sh
```
Or manually:
```bash
docker build -t openclaw:local -f Dockerfile .
docker compose run --rm openclaw-cli onboard
docker compose up -d openclaw-gateway
```

### npm / pnpm
```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

### From source
```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw && pnpm install && pnpm ui:build && pnpm build
pnpm link --global
openclaw onboard --install-daemon
```

After install, always run `openclaw onboard --install-daemon` to set up auth, gateway, and channels.

## Config Structure Quick Reference

See `references/config-reference.md` for the complete field-by-field reference.
See `references/config-examples.md` for common patterns and examples.

### Minimal Config
```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

### Top-Level Sections

| Section | Purpose |
|---------|---------|
| `identity` | Bot name, theme, emoji |
| `agents` | Model selection, workspace, sandbox, heartbeat |
| `channels` | WhatsApp, Telegram, Discord, Slack, Signal, iMessage, etc. |
| `session` | Session scope, reset, DM scope, pruning |
| `models` | Custom providers, local models, base URLs |
| `tools` | Tool allow/deny, exec settings, elevated mode |
| `cron` | Scheduled jobs |
| `hooks` | Inbound webhooks |
| `gateway` | Port, bind, auth, reload, TLS |
| `logging` | Log level, file, redaction |
| `messages` | TTS, prefix, reactions |
| `env` | Inline env vars, shell env |
| `auth` | OAuth profiles, API key order |
| `secrets` | Secret providers (env, file, exec) |
| `skills` | Skill loading, entries, bundled skills |
| `browser` | Browser tool config |
| `plugins` | Plugin loading and config |

### Channel DM Policy Pattern (all channels share this)
```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",   // pairing | allowlist | open | disabled
      allowFrom: ["tg:123"], // for allowlist/open
    },
  },
}
```

### Model Configuration
```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["openai/gpt-5.2"],
      },
      models: {
        "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
        "openai/gpt-5.2": { alias: "GPT" },
      },
    },
  },
}
```

### Custom / Local Model Providers
```json5
{
  models: {
    mode: "merge",
    providers: {
      "my-provider": {
        baseUrl: "http://localhost:4000/v1",
        apiKey: "KEY",
        api: "openai-completions", // openai-completions | openai-responses | anthropic-messages | google-generative-ai
        models: [
          {
            id: "my-model",
            name: "My Model",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 128000,
            maxTokens: 32000,
          },
        ],
      },
    },
  },
}
```

### Sandbox Configuration
```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",    // off | non-main | all
        scope: "session",    // session | agent | shared
        workspaceAccess: "none", // none | ro | rw
      },
    },
  },
}
```

Build sandbox image: `scripts/sandbox-setup.sh`

### Session Configuration
```json5
{
  session: {
    dmScope: "per-channel-peer", // main | per-peer | per-channel-peer | per-account-channel-peer
    reset: {
      mode: "daily",   // daily | idle
      atHour: 4,
      idleMinutes: 120,
    },
  },
}
```

### Config Includes (split into files)
```json5
// ~/.openclaw/openclaw.json
{
  gateway: { port: 18789 },
  agents: { $include: "./agents.json5" },
  broadcast: {
    $include: ["./clients/a.json5", "./clients/b.json5"],
  },
}
```

### Environment Variables in Config
```json5
{
  gateway: { auth: { token: "${OPENCLAW_GATEWAY_TOKEN}" } },
  models: { providers: { custom: { apiKey: "${CUSTOM_API_KEY}" } } },
}
```

Only uppercase names matched. Missing/empty vars throw errors. Escape with `$${VAR}`.

## Key Environment Variables

| Variable | Purpose |
|----------|---------|
| `OPENCLAW_HOME` | Home directory for path resolution |
| `OPENCLAW_STATE_DIR` | Override state directory |
| `OPENCLAW_CONFIG_PATH` | Override config file path |
| `OPENCLAW_HIDE_BANNER` | Hide CLI banner |

## Gateway Hot Reload

Most config changes hot-apply without restart. Fields requiring restart:
- `gateway.*` (port, bind, auth, TLS)
- `discovery`, `canvasHost`, `plugins`

Reload mode config:
```json5
{ gateway: { reload: { mode: "hybrid", debounceMs: 300 } } }
// modes: hybrid (default) | hot | restart | off
```

## Programmatic Config Updates

```bash
# Read current config
openclaw gateway call config.get --params '{}'

# Patch (partial update, preferred)
openclaw gateway call config.patch --params '{
  "raw": "{ channels: { telegram: { groups: { \"*\": { requireMention: false } } } } }",
  "baseHash": "<hash>"
}'

# Full replace
openclaw gateway call config.apply --params '{
  "raw": "<full config>",
  "baseHash": "<hash>"
}'
```

## Detailed References

For specific topics, read the appropriate reference file:

- **Full config field reference**: Read `references/config-reference.md`
- **Config examples and patterns**: Read `references/config-examples.md`
- **Docs index for latest pages**: Fetch `https://docs.openclaw.ai/llms.txt`
- **Specific channel setup**: Fetch `https://docs.openclaw.ai/channels/<channel>.md`
- **Provider setup**: Fetch `https://docs.openclaw.ai/providers/<provider>.md`

When in doubt about any specific feature, fetch the relevant page from `https://docs.openclaw.ai/` using the llms.txt index.
