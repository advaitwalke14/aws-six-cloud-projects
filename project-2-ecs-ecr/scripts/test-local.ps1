$ErrorActionPreference = "Stop"
$name = "ecs-ecr-demo-local"
$inspectRaw = docker inspect $name 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "FAIL: Container not found."
}
$container = @($inspectRaw | ConvertFrom-Json)[0]
if ($container.State.Status -ne "running") {
    throw "FAIL: Container is not running."
}
if ($container.Config.User -ne "10001") {
    throw "FAIL: Container is not running as user 10001."
}
$response = Invoke-RestMethod -Uri "http://localhost:8082/" -TimeoutSec 5
if ($response.status -ne "ok") {
    throw "FAIL: Unexpected application status."
}
if ($response.service -ne "ecs-ecr-demo") {
    throw "FAIL: Unexpected service name."
}
Write-Host "PASS: Container is running."
Write-Host "PASS: Non-root user verified."
Write-Host "PASS: HTTP endpoint responds successfully."
Write-Host "PASS: Application identity verified."
