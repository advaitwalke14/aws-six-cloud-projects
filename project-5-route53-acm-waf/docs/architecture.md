# Architecture and deployment design

## Request flow

```text
Client
  |
  | HTTPS (HTTP redirected to HTTPS)
  v
Route 53 failover DNS
  |-- primary healthy --> Primary CloudFront distribution
  `-- primary unhealthy -> Maintenance CloudFront distribution
                                  |
                                  v
                         Static maintenance content
```

If dynamic application traffic is required, CloudFront may forward to an ALB over HTTPS. Associate a regional WAF web ACL with that ALB. Associate a CloudFront-scope WAF web ACL with the CloudFront distribution.

## Certificate region rule

- CloudFront viewer certificates from ACM must be in `us-east-1`.
- ALB certificates must be in the same Region as the ALB.

## Zero-cost project boundary

This project demonstrates the decision logic and documents the intended architecture locally. It does not deploy AWS services. A real deployment may require a registered domain, Route 53 hosted zone/health checks, CloudFront, an ALB, WAF, logging, and data transfer; check current pricing before deployment.

## Operational caveats

- DNS failover is affected by TTL and resolver caching; it is not an instantaneous switch.
- Use a dedicated static maintenance origin to avoid routing failures back to the unhealthy primary.
- HSTS should be enabled only after HTTPS is confirmed across the entire hostname scope.
- Avoid HSTS preload unless the domain owner understands the long-term browser implications.
- WAF managed rule groups should be tested in COUNT mode first.
