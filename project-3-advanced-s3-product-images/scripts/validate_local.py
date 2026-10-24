import json
import subprocess
import sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
required = [
    "app.py",
    "requirements.txt",
    "README.md",
    "lifecycle-template.json",
    "scan-with-clamav.ps1",
    "tests/test_app.py",
    "configs/lifecycle-advanced-reference.json",
    "configs/s3-inventory-reference.json",
    "docs/cloudfront-private-s3-design.md",
    "docs/malware-scanning-design.md",
]
failed = False
for item in required:
    if (root / item).is_file():
        print(f"PASS: File exists: {item}")
    else:
        print(f"FAIL: Missing file: {item}")
        failed = True
json_files = [
    "lifecycle-template.json",
    "configs/lifecycle-advanced-reference.json",
    "configs/s3-inventory-reference.json",
]
for item in json_files:
    try:
        with (root / item).open(encoding="utf-8-sig") as f:
            json.load(f)
        print(f"PASS: Valid JSON: {item}")
    except (OSError, ValueError) as exc:
        print(f"FAIL: Invalid JSON: {item}: {exc}")
        failed = True
try:
    with (root / "lifecycle-template.json").open(encoding="utf-8-sig") as f:
        basic = json.load(f)
    rules = {r["ID"]: r for r in basic["Rules"]}
    assert rules["expire-demo-uploads"]["Status"] == "Enabled"
    assert rules["expire-demo-uploads"]["Filter"]["Prefix"] == "temporary/"
    assert rules["expire-demo-uploads"]["Expiration"]["Days"] == 7
    with (root / "configs/lifecycle-advanced-reference.json").open(
        encoding="utf-8-sig"
    ) as f:
        advanced = json.load(f)
    rules = {r["ID"]: r for r in advanced["Rules"]}
    transitions = rules["archive-product-images-example"]["Transitions"]
    assert [(x["Days"], x["StorageClass"]) for x in transitions] == [
        (30, "INTELLIGENT_TIERING"),
        (180, "GLACIER"),
    ]
    print("PASS: Lifecycle rules match expected reference settings.")
except (OSError, ValueError, KeyError, AssertionError) as exc:
    print(f"FAIL: Lifecycle validation: {exc}")
    failed = True
try:
    with (root / "app.py").open(encoding="utf-8-sig") as f:
        compile(f.read(), "app.py", "exec")
    with (root / "tests/test_app.py").open(encoding="utf-8-sig") as f:
        compile(f.read(), "tests/test_app.py", "exec")
    print("PASS: Python syntax.")
except (OSError, SyntaxError) as exc:
    print(f"FAIL: Python syntax: {exc}")
    failed = True
print("\nRunning automated tests:")
result = subprocess.run(
    [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
    cwd=root,
)
if result.returncode == 0:
    print("PASS: Automated test suite.")
else:
    print("FAIL: Automated test suite.")
    failed = True
if failed:
    print("\nVALIDATION FAILED")
    sys.exit(1)
print("\nVALIDATION PASSED")
print("Scope: local files and mocked/local tests only; no AWS deployment performed.")
