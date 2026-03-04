# OpenClaw Configuration Reference

Complete field-by-field reference for `~/.openclaw/openclaw.json`. JSON5 format (comments + trailing commas). All fields optional.

---

## identity

- `name`: string - bot display name
- `theme`: string - personality theme (e.g. `"helpful assistant"`)
- `emoji`: string - bot emoji

```json5
{ name: "Atlas", theme: "helpful assistant", emoji: "🤖" }
```

---

## env

- `OPENROUTER_API_KEY`, etc: inline env vars (top-level keys)
- `vars`: object of additional env vars
- `shellEnv`: `{ enabled: bool, timeoutMs: number }` - load shell env

```json5
{
  OPENROUTER_API_KEY: "sk-...",
  vars: { MY_VAR: "value" },
  shellEnv: { enabled: true, timeoutMs: 5000 },
}
```

---

## auth

- `profiles`: map of auth profile IDs to `{ provider, mode, email? }`
  - `mode`: `"oauth"` | `"api_key"`
- `order`: map of provider to ordered array of profile IDs (failover order)

```json5
{
  profiles: {
    main: { provider: "openrouter", mode: "api_key" },
    backup: { provider: "openai", mode: "oauth", email: "me@example.com" },
  },
  order: { openrouter: ["main"], openai: ["backup"] },
}
```

---

## logging

- `level`: `"info"` | `"debug"` | `"warn"` | `"error"`
- `file`: log file path (default: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`)
- `consoleLevel`: same values as `level`
- `consoleStyle`: `"pretty"` | `"compact"` | `"json"`
- `redactSensitive`: `"off"` | `"tools"`
- `redactPatterns`: array of regex strings

```json5
{
  level: "info",
  consoleStyle: "pretty",
  redactSensitive: "tools",
  redactPatterns: ["sk-[a-zA-Z0-9]+"],
}
```

---

## messages

- `messagePrefix`: string
- `responsePrefix`: string
- `ackReaction`: emoji string
- `ackReactionScope`: string
- `tts`: `{ auto, mode, provider, elevenlabs: {...}, openai: {...} }`

```json5
{
  messagePrefix: "[Bot]",
  ackReaction: "👀",
  tts: { auto: false, mode: "standard", provider: "openai" },
}
```

---

## routing

- `groupChat`: `{ mentionPatterns: string[], historyLimit: number }`
- `queue`: `{ mode, debounceMs, cap, drop, byChannel: {...} }`

```json5
{
  groupChat: { mentionPatterns: ["@bot"], historyLimit: 50 },
  queue: { mode: "fifo", debounceMs: 500, cap: 100, drop: "oldest" },
}
```

---

## agents

### agents.defaults

- `workspace`: path
- `model`: `{ primary: "provider/model", fallbacks: [...] }`
- `imageModel`: `{ primary: "provider/model" }`
- `models`: map of model IDs to `{ alias, params? }`
- `thinkingDefault`: `"off"` | `"low"` | `"medium"` | `"high"`
- `verboseDefault`: `"off"` | `"on"`
- `elevatedDefault`: `"off"` | `"on"`
- `blockStreamingDefault`: `"on"` | `"off"`
- `blockStreamingBreak`: `"text_end"` | `"message_end"`
- `blockStreamingChunk`: `{ minChars, maxChars }`
- `blockStreamingCoalesce`: `{ idleMs }`
- `humanDelay`: `{ mode: "off" | "natural" | "custom" }`
- `timeoutSeconds`: number
- `mediaMaxMb`: number
- `maxConcurrent`: number
- `userTimezone`: IANA timezone string
- `heartbeat`: `{ every, model, target, directPolicy, to, prompt, ackMaxChars }`
- `memorySearch`: `{ provider, model, remote: { apiKey }, extraPaths }`
- `sandbox`: see [Sandbox section](#agentsdefaultssandbox)
- `cliBackends`: map of backend ID to `{ command, args, output, modelArg, ... }`

```json5
{
  workspace: "~/projects",
  model: { primary: "openrouter/anthropic/claude-sonnet-4-20250514", fallbacks: ["openai/gpt-4o"] },
  thinkingDefault: "medium",
  timeoutSeconds: 120,
  maxConcurrent: 3,
  userTimezone: "America/New_York",
}
```

### agents.list

Array of agent objects: `{ id, default?, workspace?, params?, ... }`

```json5
[
  { id: "coder", default: true, workspace: "~/code" },
  { id: "writer", workspace: "~/writing", params: { temperature: 0.7 } },
]
```

---

## agents.defaults.sandbox

- `mode`: `"off"` | `"non-main"` | `"all"`
- `scope`: `"session"` | `"agent"` | `"shared"`
- `workspaceAccess`: `"none"` | `"ro"` | `"rw"`
- `perSession`: bool
- `workspaceRoot`: path

### sandbox.docker

- `image`: string (default: `"openclaw-sandbox:bookworm-slim"`)
- `workdir`: string
- `readOnlyRoot`: bool
- `tmpfs`: string[]
- `network`: string (default: `"none"`)
- `user`: `"uid:gid"`
- `env`: env var map
- `setupCommand`: string (runs once on container creation)
- `binds`: string[] (`"host:container:mode"`)
- `seccompProfile`, `apparmorProfile`: string
- `dns`, `extraHosts`: string[]

### sandbox.browser

- `enabled`: bool
- `image`, `network`, `cdpPort`, `vncPort`, `noVncPort`: various
- `headless`: bool
- `enableNoVnc`: bool
- `autoStart`: bool
- `allowHostControl`: bool

### sandbox.prune

- `idleHours`: number
- `maxAgeDays`: number

```json5
{
  mode: "non-main",
  scope: "session",
  workspaceAccess: "ro",
  docker: {
    image: "openclaw-sandbox:bookworm-slim",
    network: "none",
    readOnlyRoot: true,
    tmpfs: ["/tmp"],
    setupCommand: "apt-get update && apt-get install -y curl",
  },
  browser: { enabled: true, headless: true, autoStart: false },
  prune: { idleHours: 24, maxAgeDays: 7 },
}
```

---

## channels

All channels share: `enabled`, `dmPolicy` (`pairing` | `allowlist` | `open` | `disabled`), `allowFrom`, `groupPolicy`, `groupAllowFrom`, `groups`

### channels.whatsapp

- `allowFrom`: phone number array
- `groups`: `{ "*": { requireMention: bool } }`

### channels.telegram

- `botToken`: string
- `allowFrom`: user ID array

### channels.discord

- `token`: string
- `dm`: `{ enabled, allowFrom }`
- `guilds`: map of guild ID to `{ slug, requireMention, channels: { name: { allow, requireMention } } }`

### channels.slack

- `botToken`: `"xoxb-..."`
- `appToken`: `"xapp-..."`
- `channels`: map
- `dm`: `{ enabled, allowFrom }`
- `slashCommand`: `{ enabled, name, sessionPrefix, ephemeral }`

### channels.signal

- `dmPolicy`, `allowFrom`

### channels.imessage

- Spawns `imsg rpc` (JSON-RPC over stdio)

### channels.googlechat

- `serviceAccountFile` or `serviceAccount` or `serviceAccountRef`
- `audienceType`: `"app-url"` | `"project-number"`
- `botUser`, `dm`, `groupPolicy`, `groups`

### Other channels

`matrix`, `mattermost`, `msteams`, `irc`, `nostr`, `bluebubbles`, `synology-chat`, `line`, `feishu`, `zalo`, `tlon`, `twitch`, `nextcloud-talk` - each has channel-specific fields. Fetch docs for specifics.

```json5
{
  discord: {
    token: "Bot ...",
    dm: { enabled: true, allowFrom: ["123456"] },
    guilds: {
      "999888777": {
        slug: "my-server",
        requireMention: true,
        channels: { general: { allow: true } },
      },
    },
  },
  slack: {
    botToken: "xoxb-...",
    appToken: "xapp-...",
    dm: { enabled: true },
    slashCommand: { enabled: true, name: "/ask" },
  },
}
```

---

## session

- `scope`: `"per-sender"`
- `dmScope`: `"main"` | `"per-peer"` | `"per-channel-peer"` | `"per-account-channel-peer"`
- `identityLinks`: map of name to array of `"channel:id"` strings
- `reset`: `{ mode: "daily" | "idle", atHour, idleMinutes }`
- `resetByType`: `{ thread, direct, group }` - each with own reset config
- `resetTriggers`: string[] (e.g. `["/new", "/reset"]`)
- `store`: path
- `parentForkMaxTokens`: number
- `maintenance`: `{ mode: "warn" | "enforce", pruneAfter, maxEntries, rotateBytes, resetArchiveRetention, maxDiskBytes, highWaterBytes }`
- `typingIntervalSeconds`: number
- `sendPolicy`: `{ default: "allow" | "deny", rules: [...] }`

```json5
{
  scope: "per-sender",
  dmScope: "per-peer",
  reset: { mode: "idle", idleMinutes: 30 },
  resetTriggers: ["/new", "/reset"],
  maintenance: { mode: "warn", maxEntries: 1000 },
}
```

---

## models

- `mode`: `"merge"` | `"replace"`
- `providers`: map of provider ID to:
  - `baseUrl`: string
  - `apiKey`: string or SecretRef
  - `api`: `"openai-completions"` | `"openai-responses"` | `"anthropic-messages"` | `"google-generative-ai"`
  - `authHeader`: bool
  - `headers`: map
  - `models`: array of `{ id, name, reasoning, input, cost, contextWindow, maxTokens }`

```json5
{
  mode: "merge",
  providers: {
    local: {
      baseUrl: "http://localhost:11434/v1",
      api: "openai-completions",
      models: [{ id: "llama3", name: "Llama 3", contextWindow: 8192 }],
    },
  },
}
```

---

## tools

- `allow`: string[] of allowed tools
- `deny`: string[] of denied tools
- `exec`: `{ backgroundMs, timeoutSec, cleanupMs }`
- `elevated`: `{ enabled, allowFrom: { channel: [...] } }`
- `sandbox`: `{ tools: { allow, deny } }` (sandbox-specific tool policy)
- `sessions_spawn.attachments`: `{ enabled, maxTotalBytes, maxFiles, maxFileBytes, retainOnSessionKeep }`
- `media`: `{ audio: { enabled, maxBytes, models, timeoutSeconds }, video: { enabled, maxBytes, models } }`

```json5
{
  allow: ["shell", "file_read", "file_write"],
  deny: ["browser"],
  exec: { timeoutSec: 60 },
  elevated: { enabled: true },
}
```

---

## cron

- `enabled`: bool
- `maxConcurrentRuns`: number
- `sessionRetention`: duration string or `false`
- `runLog`: `{ maxBytes, keepLines }`
- `store`: path

```json5
{ enabled: true, maxConcurrentRuns: 2, sessionRetention: "7d" }
```

---

## hooks

- `enabled`: bool
- `path`: string
- `token`: string
- `presets`: string[]
- `mappings`: array of `{ id?, match: { path }, action, agentId, deliver, channel, to, ... }`
- `gmail`: `{ account, label, topic, subscription, pushToken, hookUrl, ... }`

```json5
{
  enabled: true,
  token: "secret-token",
  mappings: [
    { match: { path: "/deploy" }, action: "run", agentId: "coder", channel: "slack", to: "#deploys" },
  ],
}
```

---

## gateway

- `mode`: `"local"`
- `port`: number (default: `18789`)
- `bind`: `"loopback"` | `"lan"` | `"custom"` | `"tailnet"` | `"auto"`
- `controlUi`: `{ enabled, basePath }`
- `auth`: `{ mode: "token", token, allowTailscale }`
- `tailscale`: `{ mode: "serve" | "funnel", resetOnExit }`
- `remote`: `{ url, token }`
- `reload`: `{ mode: "hybrid" | "hot" | "restart" | "off", debounceMs }`
- `http.endpoints`: `chatCompletions`, `responses` (each with `enabled`)

```json5
{
  mode: "local",
  port: 18789,
  bind: "loopback",
  auth: { mode: "token", token: "my-token" },
  reload: { mode: "hybrid", debounceMs: 300 },
}
```

---

## secrets

- `providers`: map of provider ID to `{ source: "env" | "file" | "exec", path?, command?, passEnv? }`
- `defaults`: `{ env, file, exec }` - provider IDs for each source type

### SecretRef format

```json5
{ source: "env" | "file" | "exec", provider: "default", id: "..." }
```

---

## skills

- `allowBundled`: string[]
- `load.extraDirs`: string[]
- `install`: `{ preferBrew, nodeManager }`
- `entries`: map of skill ID to `{ enabled, apiKey?, env? }`

```json5
{
  allowBundled: ["web-search", "code-exec"],
  load: { extraDirs: ["~/.openclaw/skills"] },
  entries: { "web-search": { enabled: true } },
}
```

---

## browser

Browser tool config (separate from sandbox browser). Channel-specific browser settings.

---

## plugins

- `load.paths`: string[]
- `allow`, `deny`: string[]
- `entries`: map of plugin ID to `{ apiKey?, env?, config? }`
- `slots.memory`: plugin ID or `"none"`

```json5
{
  load: { paths: ["~/.openclaw/plugins"] },
  entries: { "my-plugin": { config: { key: "value" } } },
  slots: { memory: "my-memory-plugin" },
}
```

---

## bindings (multi-agent routing)

Array of `{ agentId, match: { channel, accountId?, peer?, guildId?, teamId? } }`

```json5
[
  { agentId: "support", match: { channel: "discord", guildId: "123" } },
  { agentId: "personal", match: { channel: "telegram", peer: "456" } },
]
```

---

## cli

- `banner.taglineMode`: `"random"` | `"default"` | `"off"`

---

## Config $include

Supports splitting config across multiple files.

```json5
{
  agents: { $include: "./agents.json5" },
  broadcast: { $include: ["./a.json5", "./b.json5"] },
}
```

- **Single file**: replaces containing object
- **Array**: deep-merged in order
- **Sibling keys**: merged after includes
- **Nested**: up to 10 levels
- **Paths**: relative to including file, must stay inside config dir
