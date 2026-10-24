$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$required = @(
    "README.md",
    "edge_simulator.py",
    "lambda/index.js",
    "configs/cache-policy.json",
    "configs/cloudfront-reference.json",
    "docs/architecture.md",
    "scripts/optimize_images.py",
    "scripts/run_demo.py",
    "scripts/simulate_cache_regions.py",
    "scripts/validate_config.py",
    "tests/test_edge_simulator.py",
    "tests/test_lambda_edge.js"
)
foreach ($file in $required) {
    if (-not (Test-Path $file -PathType Leaf)) {
        throw "FAIL: Missing file: $file"
    }
    Write-Host "PASS: $file"
}
Write-Host "`nChecking JavaScript syntax..."
node --check .\lambda\index.js
if ($LASTEXITCODE -ne 0) { throw "Lambda JavaScript syntax failed." }
node --check .\tests\test_lambda_edge.js
if ($LASTEXITCODE -ne 0) { throw "JavaScript test syntax failed." }
Write-Host "`nChecking Python syntax..."
py -m py_compile .\edge_simulator.py .\scripts\run_demo.py .\scripts\simulate_cache_regions.py .\scripts\validate_config.py .\scripts\optimize_images.py .\tests\test_edge_simulator.py
if ($LASTEXITCODE -ne 0) { throw "Python syntax check failed." }
Write-Host "`nValidating configuration..."
py .\scripts\validate_config.py
if ($LASTEXITCODE -ne 0) { throw "Configuration validation failed." }
Write-Host "`nRunning Python unit tests..."
py -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw "Python tests failed." }
Write-Host "`nRunning JavaScript handler tests..."
node .\tests\test_lambda_edge.js
if ($LASTEXITCODE -ne 0) { throw "JavaScript tests failed." }
Write-Host "`nRunning local edge demo..."
py .\scripts\run_demo.py
if ($LASTEXITCODE -ne 0) { throw "Edge demo failed." }
Write-Host "`nRunning synthetic cache simulation..."
py .\scripts\simulate_cache_regions.py
if ($LASTEXITCODE -ne 0) { throw "Cache simulation failed." }
Write-Host "`nPROJECT 6 LOCAL VALIDATION PASSED"
Write-Host "No AWS deployment was performed."
