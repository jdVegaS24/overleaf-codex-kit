---
name: overleaf-paper-sync
description: Work with Overleaf projects cloned through Overleaf Git integration. Use when Codex needs to connect, inspect, edit, validate, commit, pull, rebase, or push LaTeX paper changes so they appear in Overleaf after Recompile; when a user mentions Codex + Overleaf + Git, Overleaf Git tokens, scientific paper editing in an Overleaf repository, or automatic manuscript updates back to Overleaf.
---

# Overleaf Paper Sync

## Goal

Make local Codex edits land in the user's Overleaf project through Git. After a successful push, the user should be able to open Overleaf and click Recompile to see the changes.

## Decision Flow

1. If the repository is not cloned yet, read `references/setup-guide.md` and guide the user through the minimal setup. Never ask the user to paste an Overleaf token into chat; use the setup script or Git credential prompt.
2. If already inside a paper repository, run the helper script's `doctor` command to confirm the repo, remote, branch, status, and likely main `.tex` files.
3. Whenever the user asks for an edit or revision, automatically run `preflight` first to pull the latest Overleaf state unless the worktree has uncommitted user changes. If dirty, inspect and preserve those changes before editing.
4. Make the requested paper edits, keeping LaTeX structure and bibliography files intact.
5. Validate locally with conflict-marker checks and `git diff --check`. Compile only when a local TeX toolchain is available or the user asks for it; Overleaf remains the canonical compile environment.
6. Automatically run `sync` at the end unless the user explicitly asks not to push. Report the pushed commit hash and tell the user to Recompile in Overleaf.

## Commands

Use the bundled helper from the repository root or from any subdirectory inside the clone:

```bash
python scripts/overleaf_sync.py doctor .
python scripts/overleaf_sync.py preflight .
python scripts/overleaf_sync.py sync . --message "Codex: revise introduction"
```

If `python` is unavailable, use the Python executable available in the environment. On Codex desktop, `load_workspace_dependencies` can reveal a bundled Python path.

## Safety Rules

- Do not place Overleaf tokens in files, commit messages, shell history, or Git remote URLs. The remote should look like `https://git@git.overleaf.com/<project-id>` or the Server Pro equivalent, not like a URL containing a token.
- Prefer one small commit per Codex task. Use a clear message starting with `Codex:`.
- Always check `git status --short` before editing and before final sync.
- Pull before editing when the worktree is clean. If Overleaf or collaborators changed the paper during the session, commit locally, then rebase/pull before pushing.
- Preserve user changes. Do not reset, checkout, or delete uncommitted work unless the user explicitly requests it.
- Avoid moving or renaming files that may have Overleaf comments or Track Changes metadata unless the user explicitly asks.
- Do not introduce Git LFS, submodules inside the Overleaf project, tags, or branch-based workflows; Overleaf Git integration is intentionally limited.

## Editing Papers

When editing a manuscript:

- Identify the main file by searching for `\documentclass`.
- Keep edits scoped to the user's request unless scientific correctness or LaTeX validity requires a nearby fix.
- Maintain citation keys, labels, equation references, and figure paths unless changing them is part of the task.
- For bibliography changes, prefer editing the existing `.bib` file and preserving style.
- Use comments sparingly and only when the manuscript source benefits from them.

## Validation

Minimum checks before pushing, run automatically as part of the workflow:

```bash
python scripts/overleaf_sync.py doctor .
python scripts/overleaf_sync.py sync . --message "Codex: <short summary>"
```

The `sync` command stages all changes, checks for merge-conflict markers, runs `git diff --cached --check`, commits, rebases from the remote, and pushes. The user does not need to click anything between edit and push.

Optional checks when available:

- `latexmk -pdf <main.tex>`
- `tectonic <main.tex>`
- project-specific `make`, `just`, or CI scripts

## Setup Reference

Read `references/setup-guide.md` when the user asks how to install, clone, authenticate, teach this workflow, or connect a new Overleaf project.

## Classroom Behavior

For classroom usage, the default workflow is hands-off for the student after they invoke the skill:

1. Pull the latest Overleaf version first.
2. Make the requested edit.
3. Validate.
4. Push automatically.

Only stop for user input if the repository is not yet connected or Git requests a token/credential prompt during setup.
