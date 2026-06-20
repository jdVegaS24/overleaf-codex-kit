[CmdletBinding()]
param(
    [string]$Path = ".",
    [string]$Message = "Codex: sync Overleaf changes"
)

$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$helper = Join-Path $scriptRoot "skills\overleaf-paper-sync\scripts\overleaf_sync.py"

if (-not (Test-Path $helper)) {
    throw "No se encontro el helper de sincronizacion en: $helper"
}

& python $helper preflight $Path
& python $helper sync $Path --message $Message
