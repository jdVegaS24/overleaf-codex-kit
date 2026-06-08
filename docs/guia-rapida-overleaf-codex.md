# Guia rapida: Codex + Overleaf + Git

Repositorio del curso: [overleaf-codex-kit en GitHub](https://github.com/jdVegaS24/overleaf-codex-kit)

## 1. Descargar la skill

Opcion A, desde GitHub:

1. Abrir [overleaf-codex-kit en GitHub](https://github.com/jdVegaS24/overleaf-codex-kit).
2. Click en Code.
3. Click en Download ZIP.
4. Descomprimir el ZIP dentro de la carpeta del curso/proyecto.
5. Abrir una terminal dentro de `overleaf-codex-kit`.

## 2. Instalar la skill en Codex

Usa este prompt en Codex para instalarla globalmente, sin tocar CMD o PowerShell:

```text
Instala globalmente la skill de Codex desde https://github.com/Imbad0202/academic-research-skills-codex usando el instalador oficial de skills, para que quede disponible en cualquier proyecto.
```

Codex copiara la skill a tu instalacion local y quedara disponible en cualquier proyecto.

Despues de instalar, abrir un nuevo hilo de Codex o reiniciar Codex si la skill no aparece.

## 3. Preparar Overleaf

En Overleaf:

1. Abrir el proyecto del paper.
2. Ir a Menu o Integrations.
3. Activar o abrir Git Integration. Para generar o revisar el token de Git, abrir [Overleaf Account Settings](https://www.overleaf.com/user/settings).
4. Copiar el Git URL del proyecto.
5. Ir a Account Settings si todavia no se abrio desde el enlace anterior.
6. Generar un Git authentication token.

Importante: no pegar el token en el chat de Codex. El token se escribe solo en el prompt local de Git o del instalador.

## 4. Clonar y conectar el paper

La carpeta indicada en `TargetDir` sera la carpeta del paper. Crear o abrir Codex apuntando a esa carpeta para editar y subir cambios a Overleaf. No abrir `overleaf-codex-kit` para editar el paper; esa carpeta solo instala la skill.

En Windows, `$HOME\Documents` normalmente funciona aunque el Explorador muestre la carpeta como `Documentos`. Tambien se puede cambiar por otra ruta real, por ejemplo `"$HOME\Desktop\mi-paper"` o `"$HOME\mi-paper"`.

## 5. Usar Codex sobre el paper

Crear o abrir Codex apuntando a la carpeta clonada del paper, por ejemplo `$HOME\mi-paper` o la ruta indicada en `TargetDir`.

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
