"""Validate Project 5 local JSON examples; no AWS calls."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path):
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def main():
    architecture = load_json("configs/architecture.json")
    headers = load_json("configs/security_headers.json")
    waf = load_json("configs/waf_rules.json")

    assert architecture["mode"] == "local-reference-only"
    assert architecture["aws_api_calls"] is False
    assert architecture["acm"]["cloudfront_certificate_region"] == "us-east-1"
    assert headers["viewer_protocol_policy"] == "redirect-to-https"
    assert headers["strict_transport_security"]["max_age_seconds"] > 0
    assert headers["strict_transport_security"]["preload"] is False
    assert waf["recommended_initial_mode"] == "COUNT"
    assert waf["cloudfront_web_acl"]["scope"] == "CLOUDFRONT"
    assert waf["cloudfront_web_acl"]["region"] == "us-east-1"
    assert waf["alb_web_acl"]["scope"] == "REGIONAL"

    print("PASS: JSON files parsed successfully.")
    print("PASS: certificate-region and WAF-scope assumptions are consistent.")
    print("PASS: HTTPS/HSTS example is present.")
    print("PASS: WAF example recommends COUNT mode for initial testing.")
    print("No AWS API calls were made.")


if __name__ == "__main__":
    main()
