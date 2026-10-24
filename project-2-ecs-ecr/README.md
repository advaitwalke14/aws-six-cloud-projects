# ECS/ECR Demo — Python HTTP Service

## Project Overview

A Python HTTP service packaged as a Docker container for an Amazon ECS and ECR demonstration.

## Configuration

- Service name: `ecs-ecr-demo`
- Container port: `8080`
- Local port: `8082`
- Container user: `10001` (non-root)
- Health check: configured and verified locally
- Base image: `python:3.12-slim`
- Local port binding: `127.0.0.1:8082` only

## Build Locally

Run from this project directory:

```powershell
docker build -t ecs-ecr-demo:local .
```

## Run Locally

The following command starts the container with the security settings verified locally. Use it when no container named `ecs-ecr-demo-local` already exists.

```powershell
docker run -d --name ecs-ecr-demo-local --read-only --cap-drop ALL --security-opt no-new-privileges --memory 128m --cpus 0.5 --pids-limit 64 -p 127.0.0.1:8082:8080 ecs-ecr-demo:local
```

If the container already exists, run the verification script instead. It rebuilds the image, removes the previous container, starts a replacement, and checks its health.

```powershell
.\scripts\verify-local.ps1
```

## Test the Application

Check the HTTP endpoint:

```powershell
Invoke-RestMethod http://localhost:8082/
```

Run the local application tests:

```powershell
.\scripts\test-local.ps1
```

Inspect the container's state and security configuration:

```powershell
docker inspect ecs-ecr-demo-local --format "Status={{.State.Status}} Health={{.State.Health.Status}} User={{.Config.User}} PortBindings={{json .HostConfig.PortBindings}} ReadOnly={{.HostConfig.ReadonlyRootfs}} Memory={{.HostConfig.Memory}} PidsLimit={{.HostConfig.PidsLimit}}"
```

Expected verification includes:
- Container status: `running`
- Health: `healthy`
- Container user: `10001`
- Host port bound to `127.0.0.1:8082`
- Read-only root filesystem: enabled
- Memory limit: 134217728 bytes (128 MiB)
- Process limit: 64

## Verified Local Results

- Docker image built successfully.
- HTTP endpoint returned status `ok`.
- HTTP request returned `200 OK`.
- Container ran as non-root user `10001`.
- Docker health check reported `healthy`.
- Local application tests passed.
- Port binding was verified to use `127.0.0.1:8082`.
- Read-only root filesystem was enabled.
- Linux capabilities were dropped.
- Privilege escalation was disabled.
- Memory, CPU, and process limits were configured.

These results verify the local Docker environment; they do not establish that the application has been deployed or tested in AWS ECS.

## Existing AWS Resources Inspected

- Region: `ap-south-1` (Mumbai)
- ECR repository: `ecs-ecr-demo`
- ECS cluster: `ecs-ecr-demo-cluster`
- Task definition: `ecs-ecr-demo-task:1`
- CloudWatch log group: `/ecs/ecs-ecr-demo`

## Remaining Work

- Live ECS service deployment and application health verification.
- Live CloudWatch log verification.
- Final AWS networking and security review.

## Completion Status

**Local application and Docker testing: VERIFIED.**

**Live ECS deployment: NOT COMPLETED.**

During the reported inspection, the ECS cluster had zero active services and zero running tasks. Confirm the current AWS state before making any new deployment claims.

## Cost Note

- Local Docker builds and tests do not incur AWS service charges.
- Existing AWS resources may still incur charges independently.
- This project has not been redeployed to AWS as part of the local-only workflow.
- Check current AWS billing and available credits before creating or starting AWS resources.

## Local Container Security

The local verification script configures:

- Host port binding restricted to `127.0.0.1:8082`.
- Read-only root filesystem.
- All Linux capabilities dropped.
- Privilege escalation disabled.
- Memory limit of 128 MiB.
- CPU limit of 0.5 CPU.
- Process limit of 64.

These settings describe the verified local container configuration. They are not a substitute for reviewing the security configuration of a live ECS deployment.
