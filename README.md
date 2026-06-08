# Overleaf Codex Kit

Kit portable para que estudiantes o investigadores conecten Codex con un paper de Overleaf usando Git. La idea es simple: Codex edita el repositorio local, hace commit y push, y luego el usuario abre Overleaf y pulsa Recompile.

Guia rapida para estudiantes: [docs/guia-rapida-overleaf-codex.pdf](docs/guia-rapida-overleaf-codex.pdf)

## Requisitos

- Codex instalado.
- Git instalado.
- Acceso a Git Integration en Overleaf. En Overleaf Cloud es una funcion premium o institucional.
- Token de Git de Overleaf generado desde Account Settings.

Referencias oficiales:

- Overleaf Git integration: <https://docs.overleaf.com/integrations-and-add-ons/git-integration-and-github-synchronization/git-integration>
- Overleaf Git authentication tokens: <https://docs.overleaf.com/integrations-and-add-ons/git-integration-and-github-synchronization/git-integration/git-integration-authentication-tokens>

## Instalacion de la skill

Windows PowerShell:

```powershell
.\install.cmd
```

macOS/Linux:

```bash
bash ./install.sh
```

Esto copia `skills/overleaf-paper-sync` a `~/.codex/skills` o a `$CODEX_HOME/skills`.

## Conectar un proyecto de Overleaf

En Overleaf:

1. Abre el proyecto.
2. Activa o abre Git Integration desde Integrations/Menu.
3. Copia el Git URL o el comando `git clone`.
4. Genera tu Git authentication token en Account Settings.

Luego ejecuta:

Windows PowerShell:

```powershell
.\setup-overleaf-project.cmd -GitUrl "https://git@git.overleaf.com/PROJECT_ID" -TargetDir "$HOME\Documents\paper"
```

macOS/Linux:

```bash
bash ./setup-overleaf-project.sh "https://git@git.overleaf.com/PROJECT_ID" "$HOME/Documents/paper"
```

El token se pide en un prompt local. No lo pegues en Codex ni lo guardes en archivos.

Si PowerShell bloquea un `.ps1` por no estar firmado, usa los comandos `.cmd` anteriores. Ejecutan el script con una excepcion solo para ese proceso.

## Uso en Codex

Abre Codex en la carpeta clonada del paper y pide, por ejemplo:

```text
Usa $overleaf-paper-sync para revisar la introduccion y subir los cambios a Overleaf.
```

Cuando Codex termine, abre Overleaf y pulsa Recompile.

## Nota para clase

Overleaf Git no es un Git remoto completo: evita ramas, tags, Git LFS y submodulos dentro del proyecto. Para el curso, el flujo recomendado es lineal: pull, editar, validar, commit, push, Recompile.
