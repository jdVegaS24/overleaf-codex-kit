@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync-overleaf-project.ps1" %*
