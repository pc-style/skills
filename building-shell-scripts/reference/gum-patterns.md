# Gum Patterns for Shell Scripts

Use these patterns when a script benefits from terminal UI.

## Dependency Check

```bash
require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    printf 'Missing required command: %s\n' "$1" >&2
    printf 'Install gum: https://github.com/charmbracelet/gum\n' >&2
    exit 1
  }
}

require_cmd gum
```

## Non-Interactive Guard

```bash
is_interactive() {
  [[ -t 0 && -t 1 && "${CI:-}" != "true" ]]
}
```

Use `gum` only inside interactive paths when the script also needs CI support.

## Confirm Before Mutating

```bash
if is_interactive; then
  gum confirm "Install dependencies and modify local config?" || exit 0
elif [[ "${YES:-}" != "1" ]]; then
  printf 'Refusing to modify files non-interactively without YES=1.\n' >&2
  exit 1
fi
```

## Prompt for Input

```bash
project_name="$(gum input --placeholder 'my-project' --prompt 'Project name: ')"
[[ -n "$project_name" ]] || { printf 'Project name is required.\n' >&2; exit 1; }
```

## Pick One or Many

```bash
environment="$(gum choose development preview production)"
packages="$(printf '%s\n' bun vercel gh | gum choose --no-limit)"
```

## Filter a List

```bash
branch="$(git branch --format='%(refname:short)' | gum filter --placeholder 'Select branch')"
```

## Spinner Around Long Work

```bash
gum spin --title 'Installing dependencies...' --show-output -- bun install
```

## Styled Status and Errors

```bash
gum style --foreground 212 --bold 'Setup complete'
gum log --level info 'Wrote .env.local'
gum log --level error 'Missing RESEND_API_KEY'
```

## Table Output

```bash
printf 'Name,Value\nRuntime,Bun\nDeploy,Vercel\n' | gum table --separator ','
```

## Safe Wrapper Helpers

```bash
info() {
  if command -v gum >/dev/null 2>&1; then
    gum log --level info "$@"
  else
    printf 'info: %s\n' "$*"
  fi
}

confirm_or_exit() {
  local message="$1"
  if command -v gum >/dev/null 2>&1 && [[ -t 0 && -t 1 ]]; then
    gum confirm "$message" || exit 0
  else
    printf '%s [set YES=1 to continue non-interactively]\n' "$message"
    [[ "${YES:-}" == "1" ]] || exit 1
  fi
}
```
