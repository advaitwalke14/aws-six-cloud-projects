import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    with (ROOT / path).open(encoding="utf-8") as handle:
        return json.load(handle)


def main():
    architecture = load_json("configs/cloudfront-reference.json")
    cache = load_json("configs/cache-policy.json")
    assert architecture["execution_mode"] == "local-reference-only"
    assert architecture["creates_aws_resources"] is False
    assert architecture["s3_origin"]["bucket_public_access_block"] is True
    assert architecture["s3_origin"]["origin_access_control"]["enabled"] is True
    assert architecture["s3_origin"]["origin_access_control"]["signing_protocol"] == "sigv4"
    assert architecture["lambda_at_edge"]["region"] == "us-east-1"
    assert architecture["private_assets"]["use_cloudfront_signed_urls"] is True
    assert cache["local_response_rules"]["private_asset"] == "private, no-store"
    print("PASS: JSON configuration files parsed.")
    print("PASS: private S3 + OAC reference settings are consistent.")
    print("PASS: Lambda@Edge region and signed-URL intent are documented.")
    print("PASS: public and private caching rules are separated.")
    print("No AWS API calls were made.")


if __name__ == "__main__":
    main()
