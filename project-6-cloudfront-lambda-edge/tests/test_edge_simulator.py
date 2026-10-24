import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from edge_simulator import (  # noqa: E402
    cache_headers_for_path,
    inspect_request,
    make_local_signature,
    query_is_suspicious,
    simulate_regional_cache,
    validate_local_signature,
)


class QueryInspectionTests(unittest.TestCase):
    def test_clean_query_is_allowed(self):
        self.assertFalse(query_is_suspicious("campaign=spring&lang=en"))

    def test_script_query_is_suspicious(self):
        self.assertTrue(query_is_suspicious("q=%3Cscript%3Ealert(1)%3C/script%3E"))

    def test_sql_injection_pattern_is_suspicious(self):
        self.assertTrue(query_is_suspicious("q=union%20select%20password"))

    def test_path_traversal_pattern_is_suspicious(self):
        self.assertTrue(query_is_suspicious("file=..%2Fsecret.txt"))

    def test_reject_returns_403(self):
        result = inspect_request("/search", "q=%3Cscript%3E", "text/html")
        self.assertEqual(result.status_code, 403)


class ImageAndCacheTests(unittest.TestCase):
    def test_webp_rewrite_when_accepted(self):
        result = inspect_request("/images/cat.jpg", "", "image/webp,image/*")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.uri, "/images/cat.webp")

    def test_no_rewrite_without_webp_accept(self):
        result = inspect_request("/images/cat.jpg", "", "image/jpeg")
        self.assertEqual(result.uri, "/images/cat.jpg")

    def test_private_cache_is_never_public(self):
        headers = cache_headers_for_path("/private/photo.webp")
        self.assertEqual(headers["Cache-Control"], "private, no-store")

    def test_static_assets_get_shared_cache_control(self):
        headers = cache_headers_for_path("/images/cat.webp")
        self.assertIn("s-maxage=86400", headers["Cache-Control"])


class LocalSignatureTests(unittest.TestCase):
    def test_valid_short_lived_signature(self):
        secret = "unit-test-secret"
        path = "/private/photo.jpg"
        token = make_local_signature(path, 300, secret, now=1000)
        self.assertTrue(validate_local_signature(path, token, secret, now=1001))

    def test_expired_signature_rejected(self):
        secret = "unit-test-secret"
        path = "/private/photo.jpg"
        token = make_local_signature(path, 10, secret, now=1000)
        self.assertFalse(validate_local_signature(path, token, secret, now=1010))

    def test_tampered_path_rejected(self):
        secret = "unit-test-secret"
        token = make_local_signature("/private/photo.jpg", 300, secret, now=1000)
        self.assertFalse(validate_local_signature("/private/other.jpg", token, secret, now=1001))

    def test_missing_private_token_rejected(self):
        result = inspect_request("/private/photo.jpg", "", "image/jpeg", now=1000)
        self.assertEqual(result.status_code, 403)

    def test_token_ttl_limit(self):
        with self.assertRaises(ValueError):
            make_local_signature("/private/a.jpg", 901, "secret", now=1000)


class CacheRatioTests(unittest.TestCase):
    def test_regional_report_calculates_hits(self):
        report = simulate_regional_cache({"Test region": ["/a", "/b", "/a", "/b"]}, ttl_seconds=60)
        self.assertEqual(report["Test region"]["requests"], 4)
        self.assertEqual(report["Test region"]["hits"], 2)
        self.assertEqual(report["Test region"]["misses"], 2)
        self.assertEqual(report["Test region"]["hit_ratio_percent"], 50.0)


if __name__ == "__main__":
    unittest.main()
