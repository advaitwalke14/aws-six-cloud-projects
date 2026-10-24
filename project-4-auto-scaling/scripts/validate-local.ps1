$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$required = @(
    "chaos_simulation.py",
    "README.md",
    "examples/lifecycle-hook-notes.json",
    "templates/mixed-instances-asg.example.yaml",
    "tests/test_chaos_simulation.py"
)
foreach ($file in $required) {
    if (-not (Test-Path $file -PathType Leaf)) {
        throw "FAIL: Missing required file: $file"
    }
    Write-Host "PASS: $file"
}
try {
    Get-Content ".\examples\lifecycle-hook-notes.json" -Raw |
        ConvertFrom-Json | Out-Null
    Write-Host "PASS: Lifecycle-hook JSON is valid."
}
catch {
    throw "FAIL: Lifecycle-hook JSON is invalid. $($_.Exception.Message)"
}
Write-Host "`nRunning automated tests..."
py -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw "FAIL: Automated tests." }
Write-Host "`nRunning local chaos simulation..."
py .\chaos_simulation.py
if ($LASTEXITCODE -ne 0) { throw "FAIL: Chaos simulation." }
Write-Host "`nPROJECT 4 LOCAL VALIDATION PASSED"
Write-Host "Scope: local simulation and file checks; no AWS deployment performed."
