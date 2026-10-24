from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from edge_simulator import inspect_request, make_local_signature  # noqa: E402


def main():
    print("PROJECT 6 — LOCAL CLOUDFRONT / LAMBDA@EDGE SIMULATION")
    print("No AWS API calls are made; no resources are created.\n")

    samples = [
        ("/images/cat.jpg", "", "image/webp,image/*"),
        ("/index.html", "campaign=spring", "text/html"),
        ("/search", "q=%3Cscript%3Ealert(1)%3C/script%3E", "text/html"),
    ]
    for uri, query, accept in samples:
        result = inspect_request(uri, query, accept)
        print(f"{uri}?{query} => status={result.status_code}, uri={result.uri}, reason={result.reason}")
        if result.cache_control:
            print(f"  Cache-Control: {result.cache_control}")

    secret = "local-demo-secret-change-me"
    token = make_local_signature("/private/report.jpg", 300, secret, now=1_800_000_000)
    result = inspect_request("/private/report.jpg", token, "image/jpeg", secret=secret, now=1_800_000_001)
    print(f"\nPrivate asset with valid 5-minute local token => status={result.status_code}")
    print("NOTE: local HMAC token is a test stand-in, not a CloudFront native signed URL.")


if __name__ == "__main__":
    main()
