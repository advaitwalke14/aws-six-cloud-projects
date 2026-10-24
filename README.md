# AWS Cloud Projects — Six-Project Portfolio
A collection of six cloud engineering projects covering database security, containerization, object storage, Auto Scaling, DNS and web security, and content delivery.
## Project Status
These projects combine local testing, configuration validation, simulations, and selected read-only AWS inspections. **Not all six projects have been deployed to live AWS infrastructure.** Each project README describes its setup, validation, and limitations.
| # | Project | Current evidence |
|---|---|---|
| 1 | Secure MySQL on EC2 | Required local files validated; AWS configuration reviewed. Database TLS, EBS encryption, and backup restoration remain unverified. |
| 2 | ECS and ECR Container Demo | Docker image builds successfully; local container health, non-root user, and HTTP endpoint verified. Live ECS/ECR deployment not verified. |
| 3 | S3 Product Images | Local tests passed. Live AWS integration is not fully verified. |
| 4 | Auto Scaling | Local tests and simulations passed. Live Auto Scaling deployment not verified. |
| 5 | Route 53, ACM, and WAF | Local configuration and failover tests passed. Live DNS, certificate, and WAF behavior not verified. |
| 6 | CloudFront and Lambda@Edge | Local tests and simulations passed. Live CloudFront distribution and edge execution not verified. |
## Project Directories
1. [Secure MySQL on EC2](project-1-secure-mysql-ec2/README.md)
2. [ECS and ECR Container Demo](project-2-ecs-ecr/README.md)
3. [S3 Product Images](project-3-advanced-s3-product-images/README.md)
4. [Auto Scaling](project-4-auto-scaling/README.md)
5. [Route 53, ACM, and WAF](project-5-route53-acm-waf/README.md)
6. [CloudFront and Lambda@Edge](project-6-cloudfront-lambda-edge/README.md)
## Validation Evidence
Latest reported local test results:
- Project 2: Docker image build and local container verification passed.
- Project 3: 10 tests passed, plus 4 subtests.
- Project 4: 6 tests passed.
- Project 5: 6 tests passed.
- Project 6: 15 tests passed.
- Project 1: required local files check passed; database security and recovery checks remain incomplete.
These results are local validation evidence, not proof of successful production deployment.
## Safety and Cost
- Do not commit AWS credentials, private keys, passwords, or secret environment files.
- Review AWS costs and permissions before deploying resources.
- Verify network security, encryption, and backup recovery before claiming those controls are effective.
## Purpose
This portfolio demonstrates project development, cloud architecture concepts, configuration validation, local testing, troubleshooting, and documentation.
