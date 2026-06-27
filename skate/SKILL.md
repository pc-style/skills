---
name: skate
description: "Manages repository-scoped secrets and environment-variable memory with Charmbracelet skate. Use when discovering env vars, API keys, Vercel project variables, generated service credentials, or when asked to enable/disable skate-backed secret memory for a repo."
---

# Skate Secret Memory

Use Charmbracelet `skate` as a repo-scoped key/value store for environment-variable sources, generated API keys, and deployment credentials that should not be committed.

## Core Rule

Whenever this skill is enabled for a repository and you discover, generate, or configure environment variables or API keys, save a concise record in that repository's skate DB.

Do not print secret values back to the user unless they explicitly ask and it is necessary. Prefer storing and retrieving values through `skate`.

## Helper Script

Use `scripts/skate-env.py` from this skill directory.

```bash
python3 skate/scripts/skate-env.py status
python3 skate/scripts/skate-env.py enable
python3 skate/scripts/skate-env.py disable
python3 skate/scripts/skate-env.py set RESEND_API_KEY --source resend --notes "Created for transactional email"
python3 skate/scripts/skate-env.py get RESEND_API_KEY
python3 skate/scripts/skate-env.py list
```

The script derives a stable repo-specific DB name from the git root path and remote URL, so different repositories get different skate databases.

## Enable or Disable for a Repository

- Enable: run `python3 skate/scripts/skate-env.py enable` from inside the repo.
- Disable: run `python3 skate/scripts/skate-env.py disable` from inside the repo.

Enable adds a managed reminder block to the repo's `AGENTS.md`. Disable removes that block. Do not edit unrelated `AGENTS.md` content.

## What to Store

Store records when you encounter:

- `.env`, `.env.local`, `.env.example`, framework env docs, deployment env settings, or CI secret names.
- Vercel environment variables read from or written to a project.
- API keys generated through provider CLIs or dashboards.
- SMTP, Resend, Stripe, Convex, database, OAuth, webhook, and similar credentials.

Use clear key names matching the environment variable name, for example `RESEND_API_KEY`, `DATABASE_URL`, or `VERCEL_PROJECT_ID`.

## Record Format

The helper stores JSON records with:

- `value`: the secret or value
- `source`: where it came from, such as `vercel`, `.env.local`, `resend`, or `manual`
- `notes`: short context for future agents
- `repo`: repository root
- `updated_at`: UTC timestamp

## Vercel Workflow

When adding or generating Vercel variables:

1. Add/update the variable in Vercel using the project’s established workflow.
2. Save the same value or source record in the repo skate DB.
3. If the value cannot be retrieved after creation, save the variable name, source, and a note explaining where it was configured.

## Safety

- Never commit secrets to git.
- Never write raw secrets into `AGENTS.md`.
- Avoid overwriting an existing skate value unless you intentionally rotated or replaced it.
- If `skate` is not installed, tell the user to install Charmbracelet skate before using this skill.
