[CmdletBinding()]
param(
    [string]$VaultRemote = 'https://github.com/gorhkdwj/ax-learning-vault.git',
    [switch]$SkipVaultClone,
    [switch]$PlanOnly
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Write-Step {
    param([string]$Message)
    Write-Host "[bootstrap] $Message"
}

function Stop-Bootstrap {
    param([string]$Message)
    throw "[bootstrap] $Message"
}

function Get-NormalizedRemote {
    param([string]$Remote)
    return $Remote.Trim().TrimEnd('/')
}

function Assert-NoEmbeddedCredential {
    param([string]$Remote)

    $uri = $null
    if ([System.Uri]::TryCreate($Remote, [System.UriKind]::Absolute, [ref]$uri) -and
        $uri.Scheme -in @('http', 'https') -and
        -not [string]::IsNullOrEmpty($uri.UserInfo)) {
        Stop-Bootstrap "Vault 원격 URL에 사용자명이나 토큰을 포함하지 마십시오. Git 자격 증명 저장소를 사용한 뒤 다시 실행하십시오."
    }
}

$publicRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$workspaceRoot = [System.IO.Directory]::GetParent($publicRoot).FullName
$templateRoot = Join-Path $publicRoot 'templates\workspace-root'
$vaultRoot = Join-Path $workspaceRoot 'ax-learning-vault'
$workspaceGit = Join-Path $workspaceRoot '.git'
$entryPointNames = @('AGENTS.md', 'CLAUDE.md', 'README.md')

Assert-NoEmbeddedCredential $VaultRemote

if (Test-Path -LiteralPath $workspaceGit) {
    Stop-Bootstrap "상위 작업공간에 .git이 있습니다: $workspaceRoot. 상위 디렉터리는 Git 저장소가 아니어야 하므로 아무것도 변경하지 않았습니다."
}

$conflicts = [System.Collections.Generic.List[string]]::new()
$missingEntryPoints = [System.Collections.Generic.List[string]]::new()

foreach ($name in $entryPointNames) {
    $templatePath = Join-Path $templateRoot $name
    $targetPath = Join-Path $workspaceRoot $name

    if (-not (Test-Path -LiteralPath $templatePath -PathType Leaf)) {
        Stop-Bootstrap "필수 템플릿이 없습니다: $templatePath"
    }

    if (-not (Test-Path -LiteralPath $targetPath)) {
        $missingEntryPoints.Add($name)
        continue
    }

    if (-not (Test-Path -LiteralPath $targetPath -PathType Leaf)) {
        $conflicts.Add("$name (일반 파일이 아님)")
        continue
    }

    $templateHash = (Get-FileHash -LiteralPath $templatePath -Algorithm SHA256).Hash
    $targetHash = (Get-FileHash -LiteralPath $targetPath -Algorithm SHA256).Hash
    if ($templateHash -ne $targetHash) {
        $conflicts.Add("$name (템플릿과 내용이 다름)")
    }
}

if ($conflicts.Count -gt 0) {
    Stop-Bootstrap "상위 진입점 충돌을 발견했습니다: $($conflicts -join ', '). 기존 파일을 덮어쓰지 않았습니다."
}

$vaultExists = Test-Path -LiteralPath $vaultRoot
if (-not $SkipVaultClone -and $vaultExists) {
    if (-not (Test-Path -LiteralPath $vaultRoot -PathType Container)) {
        Stop-Bootstrap "Vault 경로가 디렉터리가 아닙니다: $vaultRoot. 기존 항목을 변경하지 않았습니다."
    }

    & git -C $vaultRoot rev-parse --is-inside-work-tree 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Stop-Bootstrap "Vault 경로가 Git 저장소가 아닙니다: $vaultRoot. 기존 파일을 변경하지 않았습니다."
    }

    $actualTopLevel = (& git -C $vaultRoot rev-parse --show-toplevel 2>$null)
    if ($LASTEXITCODE -ne 0 -or
        [System.IO.Path]::GetFullPath($actualTopLevel) -ne [System.IO.Path]::GetFullPath($vaultRoot)) {
        Stop-Bootstrap "Vault 경로 자체가 Git 저장소 루트가 아닙니다: $vaultRoot. 기존 저장소를 변경하지 않았습니다."
    }

    $actualRemote = (& git -C $vaultRoot remote get-url origin 2>$null)
    if ($LASTEXITCODE -ne 0) {
        Stop-Bootstrap "Vault 저장소에 origin 원격이 없습니다: $vaultRoot. 기존 저장소를 변경하지 않았습니다."
    }

    Assert-NoEmbeddedCredential $actualRemote

    if ((Get-NormalizedRemote $actualRemote) -ine (Get-NormalizedRemote $VaultRemote)) {
        Stop-Bootstrap "Vault origin이 예상 원격과 다릅니다. 예상: $VaultRemote / 실제: $actualRemote. 원격이나 파일을 변경하지 않았습니다."
    }
}

Write-Step "Public 저장소: $publicRoot"
Write-Step "상위 작업공간: $workspaceRoot"

foreach ($name in $entryPointNames) {
    if ($missingEntryPoints.Contains($name)) {
        Write-Step "$(if ($PlanOnly) { '생성 예정' } else { '생성' }): $name"
    }
    else {
        Write-Step "변경 없음: $name"
    }
}

if ($SkipVaultClone) {
    Write-Step "Vault clone을 생략합니다."
}
elseif ($vaultExists) {
    Write-Step "기존 Vault 저장소와 origin을 확인했습니다. 변경하지 않습니다."
}
else {
    Write-Step "$(if ($PlanOnly) { 'clone 예정' } else { 'clone' }): $VaultRemote -> $vaultRoot"
}

if ($PlanOnly) {
    Write-Step "계획 점검을 완료했습니다. 파일 생성이나 clone을 수행하지 않았습니다."
    exit 0
}

if (-not $SkipVaultClone -and -not $vaultExists) {
    & git clone -- $VaultRemote $vaultRoot
    if ($LASTEXITCODE -ne 0) {
        Stop-Bootstrap "Vault clone에 실패했습니다. Private 저장소 접근 권한과 Git 자격 증명을 확인한 뒤 다시 실행하십시오. 토큰은 명령이나 파일에 기록하지 마십시오."
    }
}

foreach ($name in $missingEntryPoints) {
    Copy-Item -LiteralPath (Join-Path $templateRoot $name) -Destination (Join-Path $workspaceRoot $name)
}

Write-Step "작업공간 부트스트랩을 완료했습니다."
