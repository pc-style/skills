#!/usr/bin/env python3
"""Repo-scoped environment-variable memory backed by Charmbracelet skate."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

BEGIN = "<!-- skate-env-memory:start -->"
END = "<!-- skate-env-memory:end -->"


def run(cmd: list[str], *, input_text: str | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, input=input_text, text=True, capture_output=True, check=check)


def require_skate() -> None:
    if shutil.which("skate") is None:
        raise SystemExit("skate is not installed. Install Charmbracelet skate before using this skill.")


def repo_root() -> Path:
    result = run(["git", "rev-parse", "--show-toplevel"], check=False)
    if result.returncode == 0:
        return Path(result.stdout.strip()).resolve()
    return Path.cwd().resolve()


def remote_url(root: Path) -> str:
    result = run(["git", "-C", str(root), "remote", "get-url", "origin"], check=False)
    return result.stdout.strip() if result.returncode == 0 else ""


def db_name(root: Path) -> str:
    identity = f"{root}\n{remote_url(root)}"
    digest = hashlib.sha256(identity.encode()).hexdigest()[:16]
    return f"env-{root.name}-{digest}.db"


def key_ref(key: str, db: str) -> str:
    return f"{key}@{db}"


def agents_path(root: Path) -> Path:
    return root / "AGENTS.md"


def managed_block(db: str) -> str:
    return "\n".join(
        [
            BEGIN,
            "## Skate Environment Memory",
            "When working with environment variables, API keys, Vercel variables, or generated credentials, use the skate skill and this repo-specific DB:",
            f"`@{db}`",
            "Do not commit secrets; store secret values in skate instead.",
            END,
            "",
        ]
    )


def remove_block(text: str) -> str:
    start = text.find(BEGIN)
    if start == -1:
        return text
    end = text.find(END, start)
    if end == -1:
        return text
    end += len(END)
    while end < len(text) and text[end] in " \t\r\n":
        end += 1
    return text[:start].rstrip() + ("\n" if text[:start].strip() and text[end:].strip() else "") + text[end:].lstrip()


def enable(root: Path, db: str) -> None:
    path = agents_path(root)
    existing = path.read_text() if path.exists() else ""
    cleaned = remove_block(existing).rstrip()
    updated = (cleaned + "\n\n" if cleaned else "") + managed_block(db)
    path.write_text(updated)
    print(f"enabled skate env memory in {path}")
    print(f"db=@{db}")


def disable(root: Path) -> None:
    path = agents_path(root)
    if not path.exists():
        print(f"no AGENTS.md found at {path}")
        return
    existing = path.read_text()
    updated = remove_block(existing)
    if updated == existing:
        print(f"no managed skate block found in {path}")
        return
    path.write_text(updated)
    print(f"removed skate env memory block from {path}")


def status(root: Path, db: str) -> None:
    path = agents_path(root)
    enabled = path.exists() and BEGIN in path.read_text()
    print(json.dumps({"repo": str(root), "db": db, "enabled": enabled}, indent=2))


def set_value(root: Path, db: str, args: argparse.Namespace) -> None:
    require_skate()
    value = args.value
    if value is None:
        value = sys.stdin.read()
    record = {
        "value": value,
        "source": args.source,
        "notes": args.notes,
        "repo": str(root),
        "updated_at": dt.datetime.now(dt.UTC).isoformat(),
    }
    run(["skate", "set", key_ref(args.key, db)], input_text=json.dumps(record, indent=2))
    print(f"saved {args.key} in @{db}")


def get_value(db: str, key: str, raw: bool) -> None:
    require_skate()
    result = run(["skate", "get", key_ref(key, db)])
    text = result.stdout
    if raw:
        try:
            print(json.loads(text)["value"], end="")
        except Exception:
            print(text, end="")
    else:
        print(text, end="")


def list_values(db: str) -> None:
    require_skate()
    result = run(["skate", "list", "-k", f"@{db}"], check=False)
    if result.returncode != 0:
        print(result.stderr, end="", file=sys.stderr)
        raise SystemExit(result.returncode)
    print(result.stdout, end="")


def delete_value(db: str, key: str) -> None:
    require_skate()
    run(["skate", "delete", key_ref(key, db)])
    print(f"deleted {key} from @{db}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status")
    sub.add_parser("enable")
    sub.add_parser("disable")
    sub.add_parser("list")

    set_parser = sub.add_parser("set")
    set_parser.add_argument("key")
    set_parser.add_argument("value", nargs="?")
    set_parser.add_argument("--source", default="manual")
    set_parser.add_argument("--notes", default="")

    get_parser = sub.add_parser("get")
    get_parser.add_argument("key")
    get_parser.add_argument("--raw", action="store_true", help="print only the stored value")

    delete_parser = sub.add_parser("delete")
    delete_parser.add_argument("key")

    args = parser.parse_args()
    root = repo_root()
    db = db_name(root)

    if args.command == "status":
        status(root, db)
    elif args.command == "enable":
        enable(root, db)
    elif args.command == "disable":
        disable(root)
    elif args.command == "set":
        set_value(root, db, args)
    elif args.command == "get":
        get_value(db, args.key, args.raw)
    elif args.command == "list":
        list_values(db)
    elif args.command == "delete":
        delete_value(db, args.key)


if __name__ == "__main__":
    main()
