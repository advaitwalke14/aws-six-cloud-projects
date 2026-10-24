import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_config(name):
    with (ROOT / "configs" / name).open(encoding="utf-8") as f:
        return json.load(f)


class ConfigTests(unittest.TestCase):
    def test_cloudfront_certificate_region(self):
        config = load_config("architecture.json")
        self.assertEqual(config["acm"]["cloudfront_certificate_region"], "us-east-1")

    def test_waf_scopes(self):
        config = load_config("waf_rules.json")
        self.assertEqual(config["cloudfront_web_acl"]["scope"], "CLOUDFRONT")
        self.assertEqual(config["alb_web_acl"]["scope"], "REGIONAL")

    def test_waf_starts_in_count_mode(self):
        config = load_config("waf_rules.json")
        self.assertEqual(config["recommended_initial_mode"], "COUNT")


if __name__ == "__main__":
    unittest.main()
