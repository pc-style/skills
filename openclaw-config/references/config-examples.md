# OpenClaw Configuration Examples

Common patterns for `~/.openclaw/openclaw.json`.

## Absolute Minimum
```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

## Recommended Starter
```json5
{
  identity: { name: "Clawd", theme: "helpful assistant", emoji: "🦞" },
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: { primary: "anthropic/claude-sonnet-4-5" },
    },
  },
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
}
```

## Multi-Platform Setup
```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: {
    whatsapp: { allowFrom: ["+15555550123"] },
    telegram: {
      enabled: true,
      botToken: "YOUR_TOKEN",
      allowFrom: ["123456789"],
    },
    discord: {
      enabled: true,
      token: "YOUR_TOKEN",
      dm: { allowFrom: ["123456789012345678"] },
    },
  },
}
```

## Secure DM Mode (Multi-User)
```json5
{
  session: { dmScope: "per-channel-peer" },
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15555550123", "+15555550124"],
    },
    discord: {
      enabled: true,
      token: "YOUR_DISCORD_BOT_TOKEN",
      dm: { enabled: true, allowFrom: ["123456789012345678", "987654321098765432"] },
    },
  },
}
```

## OAuth with API Key Failover
```json5
{
  auth: {
    profiles: {
      "anthropic:subscription": { provider: "anthropic", mode: "oauth", email: "me@example.com" },
      "anthropic:api": { provider: "anthropic", mode: "api_key" },
    },
    order: {
      anthropic: ["anthropic:subscription", "anthropic:api"],
    },
  },
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["anthropic/claude-opus-4-6"],
      },
    },
  },
}
```

## Local Models Only (LM Studio / Ollama)
```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: { primary: "lmstudio/minimax-m2.5-gs32" },
    },
  },
  models: {
    mode: "merge",
    providers: {
      lmstudio: {
        baseUrl: "http://127.0.0.1:1234/v1",
        apiKey: "lmstudio",
        api: "openai-responses",
        models: [
          {
            id: "minimax-m2.5-gs32",
            name: "MiniMax M2.5 GS32",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 196608,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

## Work Bot (Restricted Access via Slack)
```json5
{
  identity: { name: "WorkBot", theme: "professional assistant" },
  agents: {
    defaults: {
      workspace: "~/work-openclaw",
      elevated: { enabled: false },
    },
  },
  channels: {
    slack: {
      enabled: true,
      botToken: "xoxb-...",
      channels: {
        "": { allow: true, requireMention: true },
      },
    },
  },
}
```

## Full Sandbox Setup
```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        scope: "session",
        workspaceAccess: "none",
        workspaceRoot: "~/.openclaw/sandboxes",
        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          workdir: "/workspace",
          readOnlyRoot: true,
          tmpfs: ["/tmp", "/var/tmp", "/run"],
          network: "none",
          user: "1000:1000",
        },
        browser: { enabled: false },
        prune: { idleHours: 24, maxAgeDays: 7 },
      },
    },
  },
}
```

## Session Configuration
```json5
{
  session: {
    scope: "per-sender",
    dmScope: "per-channel-peer",
    reset: { mode: "daily", atHour: 4, idleMinutes: 120 },
    resetByType: {
      thread: { mode: "daily", atHour: 4 },
      direct: { mode: "idle", idleMinutes: 240 },
      group: { mode: "idle", idleMinutes: 120 },
    },
    resetTriggers: ["/new", "/reset"],
    threadBindings: { enabled: true, idleHours: 24, maxAgeHours: 0 },
    maintenance: {
      mode: "warn",
      pruneAfter: "30d",
      maxEntries: 500,
      rotateBytes: "10mb",
    },
  },
}
```

## Cron Jobs
```json5
{
  cron: {
    enabled: true,
    maxConcurrentRuns: 2,
    sessionRetention: "24h",
    runLog: { maxBytes: "2mb", keepLines: 2000 },
  },
}
```

## Webhook / Hooks (Gmail Example)
```json5
{
  hooks: {
    enabled: true,
    token: "shared-secret",
    path: "/hooks",
    mappings: [
      {
        id: "gmail-hook",
        match: { path: "gmail" },
        action: "agent",
        deliver: true,
        channel: "last",
      },
    ],
    gmail: {
      account: "you@gmail.com",
      label: "INBOX",
      includeBody: true,
      maxBytes: 20000,
    },
  },
}
```

## Multi-Agent with Bindings
```json5
{
  agents: {
    list: [
      { id: "home", default: true, workspace: "~/.openclaw/workspace-home" },
      { id: "work", workspace: "~/.openclaw/workspace-work" },
    ],
  },
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
}
```

## Gateway with Auth and Tailscale
```json5
{
  gateway: {
    mode: "local",
    port: 18789,
    bind: "loopback",
    controlUi: { enabled: true, basePath: "/openclaw" },
    auth: { mode: "token", token: "gateway-token", allowTailscale: true },
    tailscale: { mode: "serve", resetOnExit: false },
    reload: { mode: "hybrid", debounceMs: 300 },
  },
}
```

## Heartbeat (Periodic Check-In)
```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        model: "anthropic/claude-sonnet-4-5",
        target: "last",
        directPolicy: "allow",
        to: "+15555550123",
      },
    },
  },
}
```

## Config Includes (Split Files)
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

## Environment Variables in Config
```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: { GROQ_API_KEY: "gsk-..." },
  },
  gateway: { auth: { token: "${OPENCLAW_GATEWAY_TOKEN}" } },
  models: { providers: { custom: { apiKey: "${CUSTOM_API_KEY}" } } },
}
```

## Secrets with External Providers
```json5
{
  secrets: {
    providers: {
      default: { source: "env" },
      filemain: {
        source: "file",
        path: "~/.openclaw/secrets.json",
        mode: "json",
      },
      vault: {
        source: "exec",
        command: "/usr/local/bin/openclaw-vault-resolver",
        passEnv: ["PATH", "VAULT_ADDR"],
      },
    },
    defaults: { env: "default", file: "filemain", exec: "vault" },
  },
}
```

## Docker Deployment Quick Reference

### Quick start
```bash
./docker-setup.sh
```

### With sandbox enabled
```bash
OPENCLAW_SANDBOX=1 ./docker-setup.sh
```

### Using pre-built image
```bash
OPENCLAW_IMAGE="ghcr.io/openclaw/openclaw:latest" ./docker-setup.sh
```

### Manual Docker flow
```bash
docker build -t openclaw:local -f Dockerfile .
docker compose run --rm openclaw-cli onboard
docker compose up -d openclaw-gateway
```

### Docker env vars
- `OPENCLAW_IMAGE` - remote image (skip local build)
- `OPENCLAW_DOCKER_APT_PACKAGES` - extra apt packages
- `OPENCLAW_EXTRA_MOUNTS` - additional bind mounts
- `OPENCLAW_HOME_VOLUME` - persist /home/node
- `OPENCLAW_SANDBOX` - enable sandbox (1|true|yes|on)
- `OPENCLAW_DOCKER_SOCKET` - custom Docker socket path
- `OPENCLAW_GATEWAY_BIND` - defaults to "lan" for Docker
