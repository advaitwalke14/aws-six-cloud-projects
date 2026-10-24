$ErrorActionPreference = "Stop"
$Image = "ecs-ecr-demo:local"
$Name = "ecs-ecr-demo-local"

docker build -t $Image .
if ($LASTEXITCODE -ne 0) { throw "Docker build failed." }

$existing = docker ps -a --filter "name=^/$Name$" --format "{{.Names}}"
if ($existing -contains $Name) {
    docker rm -f $Name | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Could not remove old container." }
}

docker run -d --name $Name --read-only --cap-drop ALL --security-opt no-new-privileges --memory 128m --cpus 0.5 --pids-limit 64 -p 127.0.0.1:8082:8080 $Image
if ($LASTEXITCODE -ne 0) { throw "Container start failed." }

$deadline = (Get-Date).AddSeconds(90)
$health = ""
while ((Get-Date) -lt $deadline) {
    $health = docker inspect $Name --format "{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}"
    if ($LASTEXITCODE -ne 0) { throw "Container inspection failed." }
    if ($health -eq "healthy") { break }
    if ($health -eq "unhealthy") { docker logs $Name; throw "Container is unhealthy." }
    Start-Sleep -Seconds 3
}
if ($health -ne "healthy") { docker logs $Name; throw "Health check timed out." }

$status = docker inspect $Name --format "{{.State.Status}}"
$user = docker inspect $Name --format "{{.Config.User}}"
if ($status -ne "running") { throw "Container is not running." }
if ($user -ne "10001") { throw "Container is not running as non-root user 10001." }

$response = Invoke-RestMethod -Uri "http://localhost:8082/" -TimeoutSec 5
if ($response.status -ne "ok" -or $response.service -ne "ecs-ecr-demo") { throw "HTTP test failed." }

Write-Host "PASS: Docker image built."
Write-Host "PASS: Container is running and healthy."
Write-Host "PASS: Non-root user verified."
Write-Host "PASS: HTTP endpoint and service identity verified."
Write-Host "Container remains running at http://localhost:8082/"
Write-Host "Cleanup command: docker rm -f ecs-ecr-demo-local"
