# Guia rapida: Codex + Overleaf + Git

Repositorio del curso: <https://github.com/jdVegaS24/overleaf-codex-kit>

Objetivo: instalar una skill en Codex para que Codex edite un paper clonado desde Overleaf por Git, haga commit/push, y luego el usuario vea los cambios en Overleaf al pulsar Recompile.

## 1. Descargar el kit

Opcion A, desde GitHub:

1. Abrir <https://github.com/jdVegaS24/overleaf-codex-kit>.
2. Click en Code.
3. Click en Download ZIP.
4. Descomprimir el ZIP.
5. Abrir una terminal dentro de la carpeta `overleaf-codex-kit`.

Opcion B, con Git:

```bash
git clone https://github.com/jdVegaS24/overleaf-codex-kit.git
cd overleaf-codex-kit
```

## 2. Instalar la skill en Codex

Windows PowerShell:

```powershell
.\install.ps1
```

macOS/Linux:

```bash
bash ./install.sh
```

Despues de instalar, abrir un nuevo hilo de Codex o reiniciar Codex si la skill no aparece.

## 3. Preparar Overleaf

En Overleaf:

1. Abrir el proyecto del paper.
2. Ir a Menu o Integrations.
3. Activar o abrir Git Integration. Para generar o revisar el token de Git, usar: <https://www.overleaf.com/user/settings>.
4. Copiar el Git URL del proyecto.
5. Ir a Account Settings si todavia no se abrio desde el enlace anterior.
6. Generar un Git authentication token.

Importante: no pegar el token en el chat de Codex. El token se escribe solo en el prompt local de Git o del instalador.

## 4. Clonar y conectar el paper

Windows PowerShell:

```powershell
.\setup-overleaf-project.ps1 `
  -GitUrl "https://git@git.overleaf.com/PROJECT_ID" `
  -TargetDir "$HOME\Documents\mi-paper"
```

macOS/Linux:

```bash
bash ./setup-overleaf-project.sh \
  "https://git@git.overleaf.com/PROJECT_ID" \
  "$HOME/Documents/mi-paper"
```

Si Git pide credenciales:

- Username: `git`
- Password: el token de Overleaf

## 5. Usar Codex sobre el paper

Abrir Codex en la carpeta clonada del paper, por ejemplo `Documents/mi-paper`.

Prompt recomendado:

```text
Usa $overleaf-paper-sync para revisar la introduccion y subir los cambios a Overleaf.
```

Otro ejemplo:

```text
Usa $overleaf-paper-sync. Corrige la seccion de metodologia, conserva las citas existentes y haz push para que pueda recompilar en Overleaf.
```

## 6. Ver los cambios en Overleaf

Cuando Codex termine:

1. Abrir el proyecto en Overleaf.
2. Pulsar Recompile.
3. Revisar el PDF generado por Overleaf.

## Problemas frecuentes

- `git` no se reconoce: instalar Git y volver a abrir la terminal.
- La skill no aparece: reiniciar Codex o abrir un nuevo hilo.
- Git pide usuario: escribir `git`.
- Git pide password: usar el token de Overleaf.
- Overleaf no muestra cambios: confirmar que Codex hizo push y luego pulsar Recompile.
- Hay conflicto de Git: pedir a Codex que use `$overleaf-paper-sync` para resolver el conflicto antes de hacer push.

## Regla de oro para clase

Usar un flujo simple: pull, editar, validar, commit, push, Recompile. Evitar ramas, tags, Git LFS y submodulos dentro del proyecto de Overleaf.
