---
name: aidr
description: Offload context-heavy but low-complexity codebase work to Aider through a thin CLI wrapper. Use when another AI agent should avoid loading large repository context for tasks like discovery, repetitive refactors, cross-file version bumps, and broad search/explain passes. Supports safe read-only scanning, scoped edit runs, model-mode routing, and setup/model diagnostics.
---

# aidr

Use `aidr` to delegate large-context, low-reasoning tasks to Aider.

## Quick Start

```bash
bash scripts/setup.sh
aidr doctor
aidr models
```

## Core Commands

- `scan <goal> [paths...]`: run read-only discovery and return minimal relevant files/symbols.
- `patch <goal> [paths...]`: run small scoped edits; defaults to dry-run unless `--apply`.
- `run <goal> [paths...]`: run a universal freeform task; defaults to dry-run unless `--apply`.
- `models`: list provider-visible Gemini models through `aider --list-models gemini/`.
- `doctor`: check `aider`, `uv`, `GEMINI_API_KEY`, and active model mappings.

## Modes

- `--mode fast`: default model `gemini-2.5-flash-lite`.
- `--mode universal`: default model `gemini-3-flash-preview`.
- `--mode advanced`: default model `gemini-3-flash-preview-2` with stronger reasoning hints.

Override defaults with:

- `AIDR_MODEL_FAST`
- `AIDR_MODEL_UNIVERSAL`
- `AIDR_MODEL_ADVANCED`

## Safe Workflow

1. Start with `aidr --mode fast scan "<goal>" [paths...]`.
2. Apply repetitive edits with `aidr --mode fast patch "<goal>" [paths...] --apply`.
3. Escalate mode only when results are insufficient.
4. Use `--aider-args "..."` for extra Aider options when required.

## Compatibility

Legacy commands remain supported and map to core commands:

- `map/find/retrieve/explain` -> `scan`
- `refactor` -> `patch`
- `task` -> `run`
