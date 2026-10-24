import json
import subprocess
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class ChaosSimulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = subprocess.run(
            [sys.executable, str(ROOT / "chaos_simulation.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        cls.output = cls.result.stdout + cls.result.stderr
    def test_simulation_exits_successfully(self):
        self.assertEqual(
            self.result.returncode,
            0,
            msg=self.output,
        )
    def test_cpu_and_request_scaling_scenarios(self):
        self.assertIn("CPU test", self.output)
        self.assertIn("After CPU scale-out", self.output)
        self.assertIn("ALB test", self.output)
        self.assertIn("After request-count scale-out", self.output)
    def test_termination_and_az_recovery(self):
        self.assertIn("manually terminate one instance", self.output)
        self.assertIn("AZ failure", self.output)
        self.assertIn("After termination recovery", self.output)
        self.assertIn("After simulated AZ recovery", self.output)
        self.assertIn(
            "PASS: local logic restored minimum capacity",
            self.output,
        )
    def test_live_aws_limitations_are_disclosed(self):
        self.assertIn("LIMITATION:", self.output)
        self.assertIn("real Spot interruptions", self.output)
class ReferenceFileTests(unittest.TestCase):
    def test_lifecycle_hook_notes_are_valid_json(self):
        path = ROOT / "examples" / "lifecycle-hook-notes.json"
        with path.open(encoding="utf-8-sig") as file:
            notes = json.load(file)
        self.assertIsInstance(notes, (dict, list))
    def test_cloudformation_reference_exists(self):
        path = ROOT / "templates" / "mixed-instances-asg.example.yaml"
        self.assertTrue(path.is_file())
if __name__ == "__main__":
    unittest.main(verbosity=2)
