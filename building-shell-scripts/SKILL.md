---
name: building-shell-scripts
description: "Builds polished, user-friendly shell scripts and install.sh flows. Use when creating or editing Bash, Zsh, POSIX sh, setup scripts, installer scripts, CLI workflows, or interactive terminal automation; prefers Charmbracelet gum unless there is a concrete reason not to."
---

# Building Shell Scripts

Create shell scripts that are safe, readable, and pleasant to run. Prefer Charmbracelet `gum` for interactive UX unless there is a real reason not to.

## Default Stance: Use Gum

When building Bash, Zsh, POSIX sh, `install.sh`, setup, release, bootstrap, or CLI workflow scripts:

1. Check whether interactivity, prompts, selection, confirmation, progress, logging, tables, styled output, file picking, or long-form input would improve the script.
2. If yes, use `gum` patterns from [`reference/gum-patterns.md`](reference/gum-patterns.md).
3. If `gum` is not installed or should not be required, either:
   - add a clear dependency check with install guidance, or
   - provide a plain-shell fallback for the specific interaction.

Do not use `gum` just to decorate non-interactive scripts that must run in CI, cron, Docker builds, remote provisioning, or minimal POSIX environments.

## Required Script Quality

- Start Bash scripts with `#!/usr/bin/env bash` and `set -euo pipefail` unless POSIX sh compatibility is required.
- Quote variables and paths.
- Use arrays for command construction in Bash.
- Validate required commands before first use.
- Avoid piping secrets through logs or styled output.
- Separate “plan/confirm” from “mutate/delete/deploy”.
- Make scripts re-runnable where practical.
- Prefer explicit flags over hidden environment assumptions.

## Install Script Pattern

For `install.sh` or bootstrap scripts:

1. Detect OS/architecture.
2. Check prerequisites.
3. Explain what will change.
4. Use `gum confirm` before destructive or global changes when running interactively.
5. Use `gum spin --show-output -- command ...` for long-running install steps.
6. Print a final summary and next command.

Keep non-interactive mode available with a flag such as `--yes` or `CI=1` when appropriate.

## When Not to Use Gum

Use plain shell instead when:

- The script must be dependency-free.
- The script runs in CI/non-TTY contexts by default.
- POSIX sh portability is a hard requirement.
- The UX improvement is purely cosmetic and adds failure risk.
- The repository already has a different established CLI UI framework.

If you skip `gum`, state the reason in a comment only when the reason is non-obvious.
