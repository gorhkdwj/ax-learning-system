$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$previousLocation = Get-Location

try {
    Set-Location -LiteralPath $repoRoot

    python tools/check_public_boundary.py
    if ($LASTEXITCODE -ne 0) {
        throw "Public repository boundary validation failed."
    }

    python tools/validate_catalog.py
    if ($LASTEXITCODE -ne 0) {
        throw "Catalog validation failed."
    }

    python tools/validate_private_sources.py
    if ($LASTEXITCODE -ne 0) {
        throw "Private source validation failed."
    }

    python -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) {
        throw "Unit tests failed."
    }
}
finally {
    Set-Location -LiteralPath $previousLocation
}
