param([Parameter(Mandatory=$true)][string]$FilePath)
$scanner = Get-Command clamscan -ErrorAction SilentlyContinue
if (-not $scanner) {
    Write-Error "ClamAV clamscan was not found. Install ClamAV and ensure clamscan is on PATH."
    exit 2
}
& $scanner.Source --no-summary $FilePath
exit $LASTEXITCODE
