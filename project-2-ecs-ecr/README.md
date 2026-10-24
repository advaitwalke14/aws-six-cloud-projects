# ECS/ECR Demo - Python HTTP Service

## Project overview
Python HTTP service packaged as a Docker container for an Amazon ECS and ECR demonstration.

## Configuration
- Service name: ecs-ecr-demo
- Container port: 8080
- Local port: 8082
- Container user: 10001 (non-root)
- Health check: configured and verified locally
- Base image: python:3.12-slim

## Build locally
```powershell
docker build -t ecs-ecr-demo:local .
```

## Run locally
```powershell
docker run -d --name ecs-ecr-demo-local -p 8082:8080 ecs-ecr-demo:local
```

## Test the application
```powershell
Invoke-RestMethod http://localhost:8082/
.\scripts\test-local.ps1
docker inspect ecs-ecr-demo-local --format "Status={{.State.Status}} Health={{.State.Health.Status}} User={{.Config.User}}"
```

## Verified local results
- HTTP endpoint returned status ok.
- HTTP request returned 200 OK.
- Docker image built successfully.
- Container ran as non-root user 10001.
- Docker health check reported healthy.
- All four automated local tests passed.

## Existing AWS resources inspected
- Region: ap-south-1 (Mumbai)
- ECR repository: ecs-ecr-demo
- ECS cluster: ecs-ecr-demo-cluster
- Task definition: ecs-ecr-demo-task:1
- CloudWatch log group: /ecs/ecs-ecr-demo

## Remaining work
- Live ECS service deployment and application health verification.
- Live CloudWatch log verification.
- Final AWS networking and security review.

## Completion status
Local application and Docker testing are complete and verified.
Live ECS deployment is not complete. The inspected cluster had zero active services and zero running tasks.

## Cost note
Local Docker builds and tests do not incur AWS service charges.
Existing AWS resources can still incur charges independently.
This project has not been redeployed to AWS as part of the local-only workflow.


## Local container security
- Port binding restricted to 127.0.0.1:8082.
- Read-only root filesystem enabled.
- Linux capabilities dropped.
- Privilege escalation disabled.
- Memory limit: 128 MiB.
- CPU limit: 0.5 CPU.
- Process limit: 64.
