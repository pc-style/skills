#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_BIN="${HOME}/.local/bin"
TARGET_EXE="${TARGET_BIN}/aidr"

if ! command -v uv >/dev/null 2>&1; then
  echo "[aidr-setup] uv is required. Install uv first: https://docs.astral.sh/uv/"
  exit 1
fi

echo "[aidr-setup] Installing/upgrading aider-chat with uv..."
if command -v python3.12 >/dev/null 2>&1; then
  AIDR_PYTHON="python3.12"
elif command -v python3.11 >/dev/null 2>&1; then
  AIDR_PYTHON="python3.11"
elif command -v python3.10 >/dev/null 2>&1; then
  AIDR_PYTHON="python3.10"
else
  AIDR_PYTHON="python3"
fi

echo "[aidr-setup] Using Python interpreter: ${AIDR_PYTHON}"
if ! uv tool install --upgrade --python "${AIDR_PYTHON}" aider-chat; then
  echo "[aidr-setup] aider-chat install failed."
  echo "[aidr-setup] If scipy wheel build fails, ensure Python 3.12 is installed and retry."
  exit 1
fi

echo "[aidr-setup] Installing aidr wrapper to ${TARGET_EXE}"
mkdir -p "${TARGET_BIN}"
cp "${SCRIPT_DIR}/aidr" "${TARGET_EXE}"
chmod +x "${TARGET_EXE}"

echo "[aidr-setup] Done."
echo "[aidr-setup] Ensure ${TARGET_BIN} is on PATH."
echo "[aidr-setup] Required env: GEMINI_API_KEY"
echo "[aidr-setup] Try: aidr scan \"repository overview\""
