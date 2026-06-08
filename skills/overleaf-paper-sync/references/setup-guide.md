# Setup Guide

Use this guide only when the user needs to connect a new Overleaf project or understand the classroom workflow.

## Minimal User Flow

1. In Overleaf, open the project.
2. Open Integrations or Menu, then choose Git.
3. Copy the Git clone command or Git URL.
4. In Overleaf Account Settings, generate a Git authentication token if the user does not already have one.
5. Install this skill with the repo's `install.ps1` or `install.sh`.
6. Run the repo's `setup-overleaf-project.ps1` or `setup-overleaf-project.sh`, paste the Git URL, and enter the token only in the secure local prompt.
7. Open Codex in the cloned paper folder.
8. Ask Codex to use `$overleaf-paper-sync` for manuscript edits and to push them to Overleaf.

## Authentication Rules

Overleaf Git uses token-based authentication. If Git asks for a username, use `git`. If Git asks for a password, use the Overleaf Git authentication token.

Never ask the user to paste the token into the Codex chat. The token should be stored by Git Credential Manager, macOS Keychain, another secure credential helper, or entered directly into Git's credential prompt.

## URL Patterns

Accepted forms:

```text
https://git@git.overleaf.com/<project-id>
https://git.overleaf.com/<project-id>
https://www.overleaf.com/project/<project-id>
git clone https://git@git.overleaf.com/<project-id> paper-name
```

Normalize Overleaf Cloud URLs to:

```text
https://git@git.overleaf.com/<project-id>
```

For Overleaf Server Pro, preserve the institution host and use the Git URL shown by Overleaf.

## Classroom Prompt Examples

```text
Usa $overleaf-paper-sync para revisar la introduccion y subir los cambios a Overleaf.
```

```text
Usa $overleaf-paper-sync. Corrige la seccion de metodologia, conserva las citas existentes y haz push para que pueda recompilar en Overleaf.
```

```text
Usa $overleaf-paper-sync para verificar el estado del repo antes de editar.
```

## Overleaf Git Caveats

Treat Overleaf as a simple remote for paper source files. Avoid branch workflows, tags, Git LFS, and submodules inside the Overleaf project. Do not rename or move files with active Overleaf comments or Track Changes unless the user explicitly accepts the risk.

When collaborators edit in Overleaf while Codex edits locally, pull/rebase before pushing. If there is a conflict, resolve it in the local clone, commit, push, then ask the user to Recompile.
