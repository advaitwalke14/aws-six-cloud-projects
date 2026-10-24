from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from edge_simulator import simulate_regional_cache  # noqa: E402


def main():
    paths = ["/images/hero.webp", "/css/site.css", "/js/app.js", "/images/logo.webp", "/fonts/site.woff2"]
    request_sequences = {
        "Region A (example)": [paths[i % len(paths)] for i in range(100)],
        "Region B (example)": [paths[(i + 2) % len(paths)] for i in range(100)],
        "Region C (example)": [paths[(i * 3) % len(paths)] for i in range(100)],
    }
    report = simulate_regional_cache(request_sequences, ttl_seconds=60)
    print("SYNTHETIC REGIONAL CACHE SIMULATION — NOT LIVE CLOUDFRONT METRICS")
    for region, metrics in report.items():
        print(
            f"{region}: requests={metrics['requests']}, hits={metrics['hits']}, "
            f"misses={metrics['misses']}, hit ratio={metrics['hit_ratio_percent']}%"
        )
    print("Real regional hit ratios require actual CloudFront logs/metrics and remote requests.")


if __name__ == "__main__":
    main()
