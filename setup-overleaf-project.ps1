[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$GitUrl,

    [string]$TargetDir,

    [string]$RemoteName = "origin",

    [switch]$NoCredentialStore
)

$ErrorActionPreference = "Stop"

function Normalize-OverleafGitUrl {
    param([string]$Value)

    $url = $Value.Trim()
    if ($url -match '^git\s+clone\s+([^\s]+)') {
        $url = $Matches[1].Trim("'`"")
    }

    if ($url -match '^https://www\.overleaf\.com/project/([^/?#\s]+)') {
        return "https://git@git.overleaf.com/$($Matches[1])"
    }

    if ($url -match '^https://git\.overleaf\.com/(.+)$') {
        return "https://git@git.overleaf.com/$($Matches[1])"
    }

    return $url
}

function Get-ProjectNameFromUrl {
    param([string]$Url)

    try {
        $uri = [Uri]$Url
        $leaf = ($uri.AbsolutePath.Trim("/") -split "/")[-1]
        if ($leaf) { return "overleaf-$leaf" }
    } catch {
    }
    return "overleaf-paper"
}

function ConvertFrom-SecureStringToPlainText {
    param([Security.SecureString]$Secure)

    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Secure)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    } finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    }
}

function Ensure-CredentialHelper {
    $helper = (& git config --global --get credential.helper) 2>$null
    if ($helper) {
        Write-Host "Git credential helper: $helper"
        return
    }

    if ($env:OS -eq "Windows_NT") {
        & git config --global credential.helper manager
        Write-Host "Git credential helper configurado: manager"
    } else {
        Write-Warning "No hay credential.helper global. Git podria pedir el token en cada operacion."
    }
}

function Store-OverleafCredential {
    param([string]$Url)

    Ensure-CredentialHelper

    $uri = [Uri]$Url
    $secureToken = Read-Host "Pega tu Overleaf Git token (no se mostrara)" -AsSecureString
    $token = ConvertFrom-SecureStringToPlainText $secureToken
    try {
        $credential = "protocol=https`nhost=$($uri.Host)`nusername=git`npassword=$token`n`n"
        $credential | & git credential approve
        Write-Host "Credencial guardada para $($uri.Host) con usuario git."
    } finally {
        $token = $null
    }
}

& git --version | Out-Host

$normalizedUrl = Normalize-OverleafGitUrl $GitUrl
if (-not $TargetDir) {
    $TargetDir = Join-Path (Get-Location) (Get-ProjectNameFromUrl $normalizedUrl)
}

if (-not $NoCredentialStore) {
    Store-OverleafCredential $normalizedUrl
}

if (Test-Path $TargetDir) {
    if (-not (Test-Path (Join-Path $TargetDir ".git"))) {
        throw "TargetDir existe pero no es un repositorio Git: $TargetDir"
    }

    Push-Location $TargetDir
    try {
        $existingRemote = (& git remote) -contains $RemoteName
        if ($existingRemote) {
            & git remote set-url $RemoteName $normalizedUrl
        } else {
            & git remote add $RemoteName $normalizedUrl
        }
    } finally {
        Pop-Location
    }
} else {
    & git clone $normalizedUrl $TargetDir
}

Push-Location $TargetDir
try {
    & git config core.fileMode false
    Write-Host ""
    Write-Host "Repositorio listo en: $((Get-Location).Path)"
    & git remote -v | Out-Host
    & git status --short | Out-Host
    Write-Host ""
    Write-Host "Abre Codex en esta carpeta y pide: Usa `$overleaf-paper-sync para editar y subir los cambios a Overleaf."
} finally {
    Pop-Location
}
