#!/usr/bin/env python3
"""Small Git helper for Overleaf paper repositories."""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys
from typing import Iterable


TEXT_SUFFIXES = {
    ".tex",
    ".bib",
    ".bst",
    ".cls",
    ".sty",
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".json",
    ".csv",
    ".tsv",
    ".py",
    ".r",
    ".m",
}

CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")


def run(
    args: list[str],
    cwd: pathlib.Path,
    *,
    check: bool = True,
    capture: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args,
        cwd=str(cwd),
        check=False,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    if check and result.returncode != 0:
        cmd = " ".join(args)
        details = (result.stderr or result.stdout or "").strip()
        raise SystemExit(f"Command failed: {cmd}\n{details}")
    return result


def git(cwd: pathlib.Path, *args: str, check: bool = True) -> str:
    result = run(["git", *args], cwd, check=check)
    return (result.stdout or "").strip()


def repo_root(path: pathlib.Path) -> pathlib.Path:
    result = run(["git", "rev-parse", "--show-toplevel"], path, check=False)
    if result.returncode != 0:
        raise SystemExit(f"Not a Git repository: {path}")
    return pathlib.Path((result.stdout or "").strip()).resolve()


def current_branch(repo: pathlib.Path) -> str:
    branch = git(repo, "branch", "--show-current", check=False)
    return branch or "HEAD"


def remote_url(repo: pathlib.Path, remote: str) -> str:
    return git(repo, "remote", "get-url", remote, check=False)


def git_status(repo: pathlib.Path) -> str:
    return git(repo, "status", "--short", check=False)


def iter_repo_files(repo: pathlib.Path) -> Iterable[pathlib.Path]:
    output = git(repo, "ls-files", "-z", check=False)
    if output:
        for raw in output.split("\0"):
            if raw:
                yield repo / raw
    else:
        for path in repo.rglob("*"):
            if path.is_file() and ".git" not in path.parts:
                yield path


def read_small_text(path: pathlib.Path) -> str | None:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return None
    try:
        if path.stat().st_size > 2_000_000:
            return None
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def find_main_tex(repo: pathlib.Path) -> list[pathlib.Path]:
    candidates: list[pathlib.Path] = []
    for path in iter_repo_files(repo):
        if path.suffix.lower() != ".tex":
            continue
        text = read_small_text(path)
        if text and "\\documentclass" in text:
            candidates.append(path.relative_to(repo))
    return candidates


def scan_conflicts(repo: pathlib.Path) -> list[str]:
    hits: list[str] = []
    for path in iter_repo_files(repo):
        text = read_small_text(path)
        if not text:
            continue
        for idx, line in enumerate(text.splitlines(), start=1):
            stripped = line.lstrip()
            if any(stripped.startswith(marker) for marker in CONFLICT_MARKERS):
                hits.append(f"{path.relative_to(repo)}:{idx}: {line[:120]}")
    return hits


def credential_helper(repo: pathlib.Path) -> str:
    local_value = git(repo, "config", "--get", "credential.helper", check=False)
    global_value = git(repo, "config", "--global", "--get", "credential.helper", check=False)
    return local_value or global_value or "(not configured)"


def doctor(args: argparse.Namespace) -> int:
    repo = repo_root(pathlib.Path(args.path).resolve())
    print(f"Repository: {repo}")
    print(f"Branch: {current_branch(repo)}")
    print(f"Remote {args.remote}: {remote_url(repo, args.remote) or '(missing)'}")
    print(f"Credential helper: {credential_helper(repo)}")

    main_files = find_main_tex(repo)
    if main_files:
        print("Main TeX candidates:")
        for path in main_files:
            print(f"  - {path}")
    else:
        print("Main TeX candidates: none found")

    status = git_status(repo)
    print("Status:")
    print(status if status else "  clean")

    conflicts = scan_conflicts(repo)
    if conflicts:
        print("Conflict markers:")
        for hit in conflicts:
            print(f"  - {hit}")
        return 2
    return 0


def preflight(args: argparse.Namespace) -> int:
    repo = repo_root(pathlib.Path(args.path).resolve())
    status = git_status(repo)
    if status and not args.allow_dirty:
        print(status)
        raise SystemExit("Worktree has local changes. Inspect them before pulling or pass --allow-dirty.")

    print("Pulling latest Overleaf state...")
    result = run(["git", "pull", "--ff-only"], repo, check=False)
    if result.returncode != 0:
        branch = current_branch(repo)
        fallback = run(["git", "pull", "--ff-only", args.remote, branch], repo, check=False)
        if fallback.returncode != 0:
            details = (fallback.stderr or result.stderr or fallback.stdout or result.stdout or "").strip()
            raise SystemExit(f"Could not fast-forward pull.\n{details}")
        print((fallback.stdout or "").strip())
    else:
        print((result.stdout or "").strip())
    return 0


def ensure_staged_changes(repo: pathlib.Path) -> bool:
    git(repo, "add", "-A")
    staged = git(repo, "diff", "--cached", "--name-status", check=False)
    if not staged:
        print("No staged changes to commit.")
        return False
    print("Staged changes:")
    print(staged)
    return True


def sync(args: argparse.Namespace) -> int:
    repo = repo_root(pathlib.Path(args.path).resolve())
    conflicts = scan_conflicts(repo)
    if conflicts:
        print("Refusing to sync while conflict markers exist:")
        for hit in conflicts:
            print(f"  - {hit}")
        return 2

    if not ensure_staged_changes(repo):
        return 0

    check_result = run(["git", "diff", "--cached", "--check"], repo, check=False)
    if check_result.returncode != 0:
        details = (check_result.stdout or check_result.stderr or "").strip()
        raise SystemExit(f"git diff --cached --check failed:\n{details}")

    git(repo, "commit", "-m", args.message)
    commit = git(repo, "rev-parse", "--short", "HEAD")
    print(f"Committed: {commit}")

    print("Rebasing latest remote changes before push...")
    rebase = run(["git", "pull", "--rebase"], repo, check=False)
    if rebase.returncode != 0:
        branch = current_branch(repo)
        rebase = run(["git", "pull", "--rebase", args.remote, branch], repo, check=False)
    if rebase.returncode != 0:
        details = (rebase.stderr or rebase.stdout or "").strip()
        raise SystemExit(f"Rebase failed. Resolve conflicts, then run sync again.\n{details}")
    if rebase.stdout:
        print(rebase.stdout.strip())

    final_commit = git(repo, "rev-parse", "--short", "HEAD")
    if final_commit != commit:
        print(f"Rebased commit: {final_commit}")

    print("Pushing to Overleaf...")
    push = run(["git", "push"], repo, check=False)
    if push.returncode != 0:
        branch = current_branch(repo)
        push = run(["git", "push", args.remote, branch], repo, check=False)
    if push.returncode != 0:
        details = (push.stderr or push.stdout or "").strip()
        raise SystemExit(f"Push failed.\n{details}")
    if push.stdout:
        print(push.stdout.strip())
    if push.stderr:
        print(push.stderr.strip())
    print("Done. Open Overleaf and click Recompile.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Git helper for Overleaf paper repositories.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor_parser = subparsers.add_parser("doctor", help="Inspect repository and Overleaf sync readiness.")
    doctor_parser.add_argument("path", nargs="?", default=".")
    doctor_parser.add_argument("--remote", default="origin")
    doctor_parser.set_defaults(func=doctor)

    preflight_parser = subparsers.add_parser("preflight", help="Pull latest state before editing.")
    preflight_parser.add_argument("path", nargs="?", default=".")
    preflight_parser.add_argument("--remote", default="origin")
    preflight_parser.add_argument("--allow-dirty", action="store_true")
    preflight_parser.set_defaults(func=preflight)

    sync_parser = subparsers.add_parser("sync", help="Commit, rebase, and push local changes to Overleaf.")
    sync_parser.add_argument("path", nargs="?", default=".")
    sync_parser.add_argument("--remote", default="origin")
    sync_parser.add_argument("--message", required=True)
    sync_parser.set_defaults(func=sync)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
