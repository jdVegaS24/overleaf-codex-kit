[CmdletBinding()]
param(
    [string]$CodexHome = $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }),
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$skillName = "overleaf-paper-sync"
$source = Join-Path $PSScriptRoot "skills\$skillName"
$destRoot = Join-Path $CodexHome "skills"
$dest = Join-Path $destRoot $skillName

if (-not (Test-Path (Join-Path $source "SKILL.md"))) {
    throw "No se encontro la skill en: $source"
}

New-Item -ItemType Directory -Force -Path $destRoot | Out-Null

if (Test-Path $dest) {
    if (-not $Force) {
        throw "La skill ya existe en $dest. Ejecuta .\install.ps1 -Force para reemplazarla."
    }
    Remove-Item -LiteralPath $dest -Recurse -Force
}

Copy-Item -LiteralPath $source -Destination $dest -Recurse

Write-Host "Skill instalada en: $dest"
Write-Host "Reinicia Codex o abre un nuevo hilo si la skill no aparece inmediatamente."
