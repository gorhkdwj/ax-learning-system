[CmdletBinding()]
param(
    # 사용할 Python 명령을 직접 지정합니다. 예: 'py -3', 'python3'
    # 생략하면 실제로 실행되는 Python 3 인터프리터를 자동으로 탐지합니다.
    [string]$PythonCommand
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$previousLocation = Get-Location

# Windows에서 `python`은 실제 인터프리터가 아니라 Microsoft Store 별칭일 수 있습니다.
# 별칭은 존재 검사만으로는 걸러지지 않으므로 실제로 실행해 Python 3인지 확인합니다.
function Test-PythonCandidate {
    param([string[]]$Command)

    $exe = $Command[0]
    $prefixArgs = @()
    if ($Command.Length -gt 1) {
        $prefixArgs = $Command[1..($Command.Length - 1)]
    }

    try {
        $probe = 'import sys; sys.stdout.write(str(sys.version_info[0]))'
        $output = & $exe @prefixArgs '-c' $probe 2>$null
        return ($LASTEXITCODE -eq 0 -and "$output".Trim() -eq '3')
    }
    catch {
        return $false
    }
}

function Resolve-PythonCommand {
    param([string]$Requested)

    if ($Requested) {
        $parts = $Requested -split '\s+' | Where-Object { $_ }
        if (Test-PythonCandidate -Command $parts) {
            return $parts
        }
        throw "Requested Python command is not a usable Python 3 interpreter: $Requested"
    }

    # 중첩 배열은 @()에서 평탄화되므로 후보를 문자열로 두고 분해합니다.
    foreach ($candidate in @('py -3', 'python3', 'python')) {
        $parts = $candidate -split '\s+' | Where-Object { $_ }
        if (Test-PythonCandidate -Command $parts) {
            return $parts
        }
    }

    throw @'
No usable Python 3 interpreter was found.
One of "py -3", "python3" or "python" must resolve to a real Python 3.
On Windows, "python" may resolve to the Microsoft Store alias; put a real Python
earlier on PATH or pass -PythonCommand explicitly.
'@
}

try {
    Set-Location -LiteralPath $repoRoot

    $python = Resolve-PythonCommand -Requested $PythonCommand
    $pythonExe = $python[0]
    $pythonArgs = @()
    if ($python.Length -gt 1) {
        $pythonArgs = $python[1..($python.Length - 1)]
    }
    Write-Host "Python interpreter: $($python -join ' ')"

    & $pythonExe @pythonArgs tools/check_public_boundary.py
    if ($LASTEXITCODE -ne 0) {
        throw "Public repository boundary validation failed."
    }

    & $pythonExe @pythonArgs tools/validate_catalog.py
    if ($LASTEXITCODE -ne 0) {
        throw "Catalog validation failed."
    }

    & $pythonExe @pythonArgs tools/validate_private_sources.py
    if ($LASTEXITCODE -ne 0) {
        throw "Private source validation failed."
    }

    & $pythonExe @pythonArgs -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) {
        throw "Unit tests failed."
    }
}
finally {
    Set-Location -LiteralPath $previousLocation
}
