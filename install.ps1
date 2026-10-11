param(
    [string]$SkillHome = '',
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

if (-not $SkillHome) {
    $TaskCodexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path ([Environment]::GetFolderPath('UserProfile')) '.codex' }
    $SkillHome = Join-Path $TaskCodexRoot 'skills'
}
$SkillsRoot = [IO.Path]::GetFullPath($SkillHome)
$PackageSkill = Join-Path $PSScriptRoot 'universal-orchestrator'
$SkillSource = (Resolve-Path -LiteralPath $PackageSkill).Path
$Destination = [IO.Path]::GetFullPath((Join-Path $SkillsRoot 'universal-orchestrator'))
$Legacy = [IO.Path]::GetFullPath((Join-Path $SkillsRoot 'luna-orchestra'))
$BackupRoot = [IO.Path]::GetFullPath((Join-Path (Split-Path $SkillsRoot -Parent) 'skill-backups'))
$Stamp = [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss-fffffff')
$RunBackup = Join-Path $BackupRoot ('universal-orchestrator-' + $Stamp)
$Prepared = Join-Path $RunBackup 'prepared-new'

function Assert-Within([string]$Target, [string]$Root) {
    $ResolvedTarget = [IO.Path]::GetFullPath($Target)
    $ResolvedRoot = [IO.Path]::GetFullPath($Root).TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
    $Prefix = $ResolvedRoot + [IO.Path]::DirectorySeparatorChar
    if (-not $ResolvedTarget.StartsWith($Prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Target outside intended directory: $ResolvedTarget"
    }
}
function Assert-RegularDirectory([string]$Target) {
    if (Test-Path -LiteralPath $Target) {
        $Item = Get-Item -LiteralPath $Target -Force
        if (-not $Item.PSIsContainer -or ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "Not a regular directory: $Target"
        }
    }
}

Assert-Within $Destination $SkillsRoot
Assert-Within $Legacy $SkillsRoot
Assert-Within $RunBackup $BackupRoot
Assert-Within $Prepared $BackupRoot
Assert-RegularDirectory $SkillsRoot
Assert-RegularDirectory $BackupRoot
Assert-RegularDirectory $SkillSource
Assert-RegularDirectory $Destination
Assert-RegularDirectory $Legacy
if (-not (Test-Path -LiteralPath (Join-Path $SkillSource 'SKILL.md') -PathType Leaf)) { throw 'Missing SKILL.md' }
$Linked = Get-ChildItem -LiteralPath $SkillSource -Recurse -Force | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }
if ($Linked) { throw 'Skill source contains links; installation aborted' }
if ($DryRun) {
    Write-Output "DRY RUN: install $SkillSource -> $Destination"
    Write-Output "Backup existing skills outside discovery: $RunBackup"
    return
}

New-Item -ItemType Directory -Path $SkillsRoot -Force | Out-Null
New-Item -ItemType Directory -Path $RunBackup -Force | Out-Null
Copy-Item -LiteralPath $SkillSource -Destination $Prepared -Recurse
$Moved = [Collections.Generic.List[object]]::new()
$OriginalDestination = Test-Path -LiteralPath $Destination
$NewInstalled = $false
try {
    foreach ($Existing in @($Legacy, $Destination)) {
        if (Test-Path -LiteralPath $Existing) {
            Assert-Within $Existing $SkillsRoot
            $Archive = Join-Path $RunBackup (Split-Path $Existing -Leaf)
            Assert-Within $Archive $BackupRoot
            Move-Item -LiteralPath $Existing -Destination $Archive
            $Moved.Add([pscustomobject]@{ Original = $Existing; Archive = $Archive })
        }
    }
    Assert-Within $Prepared $BackupRoot
    Assert-Within $Destination $SkillsRoot
    Move-Item -LiteralPath $Prepared -Destination $Destination
    $NewInstalled = $true
} catch {
    $CanonicalArchived = @($Moved | Where-Object { $_.Original -eq $Destination }).Count -gt 0
    if (($NewInstalled -or $CanonicalArchived -or -not $OriginalDestination) -and (Test-Path -LiteralPath $Destination)) {
        $Failed = Join-Path $RunBackup 'failed-new'
        Assert-Within $Destination $SkillsRoot
        Assert-Within $Failed $BackupRoot
        Move-Item -LiteralPath $Destination -Destination $Failed
    }
    for ($Index = $Moved.Count - 1; $Index -ge 0; $Index--) {
        $Previous = $Moved[$Index]
        Assert-Within $Previous.Archive $BackupRoot
        Assert-Within $Previous.Original $SkillsRoot
        Move-Item -LiteralPath $Previous.Archive -Destination $Previous.Original
    }
    throw
}
Write-Output "Installed: $Destination"
Write-Output "Backup: $RunBackup"
Write-Output 'Main conversation model and config.toml were not changed.'
