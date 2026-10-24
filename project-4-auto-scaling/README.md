# Project 4 — Auto Scaling with Mixed Instances and Chaos Testing

## ₹0 lab mode
Run `py chaos_simulation.py` on your computer. The simulator makes no AWS API calls and creates no billable resources. It represents mixed On-Demand/Spot placement, launch warm-up, CPU/request scaling events, manual termination, and an Availability Zone failure.

## Included reference template
`templates/mixed-instances-asg.example.yaml` is a CloudFormation reference for a real AWS setup. **Do not deploy it in the zero-cost lab.** A live stack requires pre-existing VPC subnets, an ALB target group/security group, and an instance profile, and running EC2/Spot, ALB and CloudWatch may incur charges.

The template includes:
- Mixed On-Demand and Spot instance policy
- Launch lifecycle hook
- CPU target tracking (70%)
- ALB requests-per-target tracking (1000)
- Instances spread across provided subnets
- IMDSv2 requirement and HTTP ingress only from the ALB security group

## Lifecycle hook limitation
The CloudFormation hook pauses launch events, but actual database migration orchestration needs an event consumer that completes the lifecycle action after migrations/readiness checks. See `examples/lifecycle-hook-notes.json`. The local simulation only represents this behavior; it does not execute a real migration.

## Run and interpret results
```powershell
py .\chaos_simulation.py
```
A successful run means the local logic restored its simulated minimum capacity after the two simulated failures. It does **not** prove live AWS zero-downtime behavior, real load handling, Spot interruption handling, or ALB health-check behavior.

## Before a live deployment
- Validate the template with CloudFormation before deployment.
- Use at least two subnets/AZs and a valid target group.
- Provide a least-privilege instance profile.
- Add and test an EventBridge + lifecycle-action completion worker.
- Estimate and approve AWS costs before creating resources.

## Validation record
- Local chaos simulation: passed.
- Automated tests: 6 passed.
- Lifecycle-hook notes JSON: parsed successfully.
- AWS CloudFormation validate-template: accepted the template body in ap-south-1.
- No CloudFormation stack was created by this validation.

## Remaining limitations
- No live Auto Scaling group or Application Load Balancer was deployed and tested.
- Real Spot interruptions, launch lifecycle-action completion, and zero downtime are not verified.
- The lifecycle-hook event consumer remains a documented design, not an implementation.
## Completion Status
**Local chaos simulation and automated tests: VERIFIED (6 tests passed).**
**CloudFormation reference template: Validation accepted in `ap-south-1`; no stack was created.**
**Live Auto Scaling group and ALB: NOT DEPLOYED.**
Real Spot interruption handling, lifecycle-action completion, and zero-downtime recovery remain unverified.
