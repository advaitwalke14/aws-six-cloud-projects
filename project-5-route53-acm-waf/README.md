# Project 5 — Route 53, ACM, CloudFront, ALB and AWS WAF

## Scope and cost boundary

This repository contains a **local, no-AWS-call reference implementation** for the Project 5 design. Running the simulator and tests does not create AWS resources and does not require AWS credentials.

**It is not a live AWS deployment.** Route 53 hosted zones and health checks, registered domains, ALBs, CloudFront distributions, ACM certificates, and AWS WAF web ACLs are not created or verified by this project. Some live components can incur charges. Do not deploy resources if maintaining a strict $0 additional spend is a requirement.

## Architecture

1. Route 53 failover policy selects the primary CloudFront endpoint while the primary health signal is healthy.
2. If the primary is unhealthy, the policy selects a maintenance CloudFront endpoint.
3. CloudFront redirects viewer HTTP requests to HTTPS and adds security response headers.
4. ACM certificates are issued in the AWS Region required by the endpoint:
   - CloudFront viewer certificate: `us-east-1`.
   - Regional ALB certificate: same Region as the ALB.
5. AWS WAF web ACLs protect CloudFront and, if used, the regional ALB. Managed rule groups are examples only and must be tested for false positives before production use.

See `docs/architecture.md` for the intended deployment design and caveats.

## Run locally

From this folder in PowerShell:

```powershell
py .\simulate_failover.py
py -m unittest discover -s tests -v
py .\scripts\validate_config.py
```

All commands are local only. The validator checks the example configuration files and makes no AWS API calls.

## Included files

- `simulate_failover.py` — pure-Python failover and HTTPS/HSTS policy simulation.
- `configs/architecture.json` — architecture, certificate-region, and WAF design examples.
- `configs/security_headers.json` — HTTPS/HSTS security-header example.
- `configs/waf_rules.json` — illustrative managed rule-group configuration.
- `scripts/validate_config.py` — local JSON/config consistency checks.
- `tests/` — unit tests for routing, security headers, and config assumptions.

## Security and production notes

- Replace example hostnames with a domain you control before any real deployment.
- Do not commit private keys, AWS credentials, account IDs, or certificate material.
- HSTS should only be enabled after HTTPS works reliably for every covered hostname. `includeSubDomains` and preload have wider consequences; preload is disabled in this example.
- WAF managed rules can block legitimate traffic. Start in count mode, inspect logs, then move selected rules to block mode.
- Route 53 health-check behavior and DNS caching mean failover is not instantaneous.
- This repository intentionally does not include a deploy command.
## Completion Status
**Local simulations and automated tests: VERIFIED.**
**Live AWS deployment: NOT COMPLETED.** Route 53, ACM, CloudFront, ALB, and WAF deployment and failover behavior remain unverified.
The project remains local-only. Do not deploy billable resources while maintaining a strict ₹0 additional-spend requirement.
