<#
    Syncs the live Foundry modules and this git repo.

      .\sync-module.ps1            # Foundry  ->  repo   (do this before committing)
      .\sync-module.ps1 -Restore   # repo     ->  Foundry (disaster recovery / new machine)

    Two modules are managed:
      icewind-dale-vagabond  ->  module/             the adventure content
      vagabond-effect-fix    ->  module-effect-fix/  system bugfix, see notes/

    IMPORTANT: shut Foundry down before running either direction. Compendium packs are
    LevelDB and buffer writes in memory - copying a pack while Foundry holds it open can
    capture a half-written database.
#>
param([switch]$Restore, [switch]$Force)

$Modules = @(
  @{ Id = "icewind-dale-vagabond"; Dir = "module" },
  @{ Id = "vagabond-effect-fix";   Dir = "module-effect-fix" }
)

# Warn if Foundry looks like it's running. What actually matters is that the WORLD has been
# shut down at least once since the packs were last written - that is when LevelDB flushes to
# disk. The server process being up is fine on its own.
if (-not $Force -and (Get-Process -Name "Foundry Virtual Tabletop","node" -ErrorAction SilentlyContinue)) {
  Write-Warning "Foundry appears to be running. Make sure the WORLD has been shut down since the packs were last modified - LevelDB only flushes to disk on a clean world shutdown."
  $ok = Read-Host "Continue? (y/N)"
  if ($ok -ne "y") { exit 1 }
}

foreach ($m in $Modules) {
  $live = Join-Path "$env:LOCALAPPDATA\FoundryVTT\Data\modules" $m.Id
  $repo = Join-Path $PSScriptRoot $m.Dir

  if ($Restore) { $from = $repo; $to = $live; $label = "repo -> Foundry" }
  else          { $from = $live; $to = $repo; $label = "Foundry -> repo" }

  if (-not (Test-Path $from)) {
    Write-Warning ("skipped {0}: source not found ({1})" -f $m.Id, $from)
    continue
  }

  New-Item -ItemType Directory -Force -Path $to | Out-Null
  # /MIR mirrors exactly (deletes files removed at source). LOCK files excluded.
  robocopy $from $to /MIR /XF LOCK /NFL /NDL /NJH /NJS /NP | Out-Null
  if ($LASTEXITCODE -ge 8) { Write-Error ("robocopy failed for {0} ({1})" -f $m.Id, $LASTEXITCODE); exit 1 }

  $files = Get-ChildItem $to -Recurse -File
  $mb = ($files | Measure-Object -Property Length -Sum).Sum / 1MB
  Write-Host ("{0,-24} {1}  |  {2} files, {3:N1} MB" -f $m.Id, $label, $files.Count, $mb) -ForegroundColor Green
}

# robocopy uses 0-7 for success (1 = files were copied). Don't leak that as a failure.
exit 0
