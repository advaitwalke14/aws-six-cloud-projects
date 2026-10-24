"""Local-only Project 5 simulation. Makes no AWS API calls."""
from dataclasses import dataclass


@dataclass(frozen=True)
class FailoverDecision:
    endpoint: str
    reason: str


def choose_endpoint(primary_healthy: bool) -> FailoverDecision:
    if primary_healthy:
        return FailoverDecision(
            endpoint="primary-cloudfront",
            reason="primary health check passed",
        )
    return FailoverDecision(
        endpoint="maintenance-cloudfront",
        reason="primary health check failed",
    )


SECURITY_POLICY = {
    "viewer_protocol_policy": "redirect-to-https",
    "hsts_enabled": True,
    "hsts_max_age_seconds": 31_536_000,
    "include_subdomains": True,
    "preload": False,
}


def main() -> None:
    print("PROJECT 5: ROUTE 53 / ACM / WAF — LOCAL SIMULATION")
    print("No AWS API calls are made; no AWS resources are created.")
    for healthy in (True, False):
        decision = choose_endpoint(healthy)
        print(
            f"Primary healthy={healthy}: route to {decision.endpoint} "
            f"({decision.reason})"
        )
    print("\nHTTPS/HSTS policy example:")
    for key, value in SECURITY_POLICY.items():
        print(f"  {key}: {value}")
    print("\nPASS: local failover decision logic executed.")
    print(
        "LIMITATION: Route 53 health checks, ACM, CloudFront, ALB and WAF "
        "are not live-tested."
    )


if __name__ == "__main__":
    main()
