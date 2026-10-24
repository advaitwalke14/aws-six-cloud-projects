$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$required = @(
    "README.md",
    "simulate_failover.py",
    "configs/architecture.json",
    "configs/hsts-policy.json",
    "configs/route53-failover-records.example.json",
    "configs/security_headers.json",
    "configs/waf_rules.json",
    "docs/architecture.md",
    "scripts/validate_config.py",
    "tests/test_config.py",
    "tests/test_failover.py"
)
foreach ($file in $required) {
    if (-not (Test-Path $file -PathType Leaf)) {
        throw "FAIL: Missing file: $file"
    }
    Write-Host "PASS: $file"
}
Write-Host "`nChecking Python syntax..."
py -m py_compile .\simulate_failover.py .\scripts\validate_config.py .\tests\test_config.py .\tests\test_failover.py
if ($LASTEXITCODE -ne 0) { throw "Python syntax check failed." }
Write-Host "`nValidating configurations..."
py .\scripts\validate_config.py
if ($LASTEXITCODE -ne 0) { throw "Configuration validation failed." }
Write-Host "`nRunning automated tests..."
py -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw "Automated tests failed." }
Write-Host "`nRunning failover simulation..."
py .\simulate_failover.py
if ($LASTEXITCODE -ne 0) { throw "Failover simulation failed." }
Write-Host "`nPROJECT 5 LOCAL VALIDATION PASSED"
Write-Host "Local tests only; live AWS features have not been deployed or verified."
