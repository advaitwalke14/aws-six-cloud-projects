$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$required = @(
    "sql\schema.sql",
    "sql\verify-tls.sql",
    "scripts\check-db.sh",
    "README.md",
    "docs\current-review.md",
    "docs\free-completion-plan.md"
)

$missing = @()
foreach ($relativePath in $required) {
    $fullPath = Join-Path $root $relativePath
    if (Test-Path $fullPath -PathType Leaf) {
        Write-Host "[PASS] $relativePath"
    } else {
        Write-Host "[MISSING] $relativePath"
        $missing += $relativePath
    }
}

if ($missing.Count -gt 0) {
    Write-Host "Local project file check FAILED. No AWS APIs were called."
    exit 1
}

Write-Host ""
Write-Host "PASS: required local files are present."
Write-Host "LIMITATION: this does not connect to AWS or verify live TLS, encryption, or backups."
Write-Host "No AWS API calls were made."
