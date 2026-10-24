import unittest
from simulate_failover import choose_endpoint, SECURITY_POLICY


class FailoverTests(unittest.TestCase):
    def test_healthy_primary(self):
        self.assertEqual(choose_endpoint(True).endpoint, "primary-cloudfront")

    def test_unhealthy_primary_uses_maintenance(self):
        self.assertEqual(
            choose_endpoint(False).endpoint, "maintenance-cloudfront"
        )

    def test_https_redirect_and_hsts(self):
        self.assertEqual(
            SECURITY_POLICY["viewer_protocol_policy"], "redirect-to-https"
        )
        self.assertTrue(SECURITY_POLICY["hsts_enabled"])
        self.assertEqual(SECURITY_POLICY["hsts_max_age_seconds"], 31536000)
        self.assertFalse(SECURITY_POLICY["preload"])


if __name__ == "__main__":
    unittest.main()
