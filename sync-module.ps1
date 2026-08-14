<#
    Syncs the live Foundry module and this git repo.

      .\sync-module.ps1            # Foundry  ->  repo   (do this before committing)
      .\sync-module.ps1 -Restore   # repo     ->  Foundry (disaster recovery / new machine)

    IMPORTANT: shut Foundry down before running either direction. Compendium packs are
    LevelDB and buffer writes in memory - copying a pack while Foundry holds it open can
    capture a half-written database.
#>
param([switch]$Restore, [switch]$Force)

$Live = "$env:LOCALAPPDATA\FoundryVTT\Data\modules\icewind-dale-vagabond"
$Repo = Join-Path $PSScriptRoot "module"

if ($Restore) {
  $from  = $Repo; $to = $Live; $label = "repo  ->  Foundry"
} else {
  $from  = $Live; $to = $Repo; $label = "Foundry  ->  repo"
}

if (-not (Test-Path $from)) { Write-Error "Source not found: $from"; exit 1 }

# Warn if Foundry looks like it's running. What actually matters is that the WORLD has been
# shut down at least once since the packs were last written - that is when LevelDB flushes to
# disk. The server process being up is fine on its own.
if (-not $Force -and (Get-Process -Name "Foundry Virtual Tabletop","node" -ErrorAction SilentlyContinue)) {
  Write-Warning "Foundry appears to be running. Make sure the WORLD has been shut down since the packs were last modified - LevelDB only flushes to disk on a clean world shutdown."
  $ok = Read-Host "Continue? (y/N)"
  if ($ok -ne "y") { exit 1 }
}

New-Item -ItemType Directory -Force -Path $to | Out-Null
# /MIR mirrors exactly (deletes files removed at source). LOCK files excluded.
robocopy $from $to /MIR /XF LOCK /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { Write-Error "robocopy failed ($LASTEXITCODE)"; exit 1 }

$files = Get-ChildItem $to -Recurse -File
$mb = ($files | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host ("{0}  |  {1} files, {2:N1} MB" -f $label, $files.Count, $mb) -ForegroundColor Green

# robocopy uses 0-7 for success (1 = files were copied). Don't leak that as a failure.
exit 0
