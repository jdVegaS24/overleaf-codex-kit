# Overleaf Codex Skill

Repositorio del curso para usar Codex con Overleaf y Git de forma transparente. La idea es simple: pega dos prompts en Codex, deja que Codex prepare la instalacion y el paper, y luego recompila en Overleaf.

Guia rapida para estudiantes: [docs/guia-rapida-overleaf-codex.pdf](docs/guia-rapida-overleaf-codex.pdf)

## Prompt 1: instalar la skill globalmente

```text
Instala globalmente la skill de Codex desde https://github.com/jdVegaS24/overleaf-codex-kit usando el instalador oficial de skills, para que quede disponible en cualquier proyecto.
```

## Flujo

1. En Overleaf, abre el proyecto que quieres modificar.
2. En Overleaf Account Settings, entra desde [https://www.overleaf.com/user/settings](https://www.overleaf.com/user/settings) y genera tu Git authentication token.
3. Copia el Git URL del proyecto.
4. Pega el Prompt 1 en Codex para instalar la skill.
5. Pega el Prompt 2 en Codex para conectar el paper y crear la carpeta de trabajo.
6. Cuando Codex termine, abre Overleaf y pulsa Recompile para ver los cambios.

## Prompt 2: conectar el paper de Overleaf

```text
Crea una carpeta nueva para este paper, conecta mi proyecto de Overleaf con Git usando este link: https://www.overleaf.com/project/PROJECT_ID, usa esa carpeta como TargetDir, y deja todo listo para editar y subir cambios sin abrir CMD o PowerShell.
```

Nota: el token se escribe en el prompt local de Git o en el instalador cuando se lo pide; no se pega en el chat de Codex. `PROJECT_ID` es el identificador del proyecto de Overleaf que quieres modificar.
