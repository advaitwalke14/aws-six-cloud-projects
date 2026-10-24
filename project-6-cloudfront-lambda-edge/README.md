# Project 6 — CloudFront + Lambda@Edge Enhancements (Local, $0 build)

## What this project demonstrates

This is a **local simulation and reference implementation**. Its normal run/test commands make no AWS API calls and create no AWS resources.

- Private S3 origin + CloudFront Origin Access Control (OAC) reference configuration.
- Lambda@Edge-style request inspection that blocks suspicious query strings.
- Rewriting image requests to pre-generated `.webp` variants when the client accepts WebP.
- Response caching-header rules.
- Short-lived signed-access simulation for `/private/` assets.
- Synthetic cache-hit-ratio calculations for three example regions.
- Optional local image conversion to WebP (requires Pillow).

## Important $0 boundary

Do not deploy AWS resources if you must guarantee **$0 additional AWS spend**. This repository does not deploy CloudFront, Lambda@Edge, S3, key groups, or distributions. Real AWS use can incur costs or consume credits. The cache report is synthetic; it is not a measurement from real CloudFront edge locations.

Native CloudFront signed URLs use CloudFront's trusted public keys/key groups and its supported signing format. The local HMAC token used here is only a test stand-in and is **not compatible with CloudFront signed URLs**. Never deploy this local HMAC scheme as a replacement for CloudFront's native signing.

## Requirements

- Python 3.10+ (standard-library implementation and tests).
- Optional: Pillow for local WebP conversion.
- Optional: Node.js if you want to run the included Lambda@Edge JavaScript syntax check or adapt it for AWS.

## Run on Windows PowerShell

From this folder:

```powershell
py .\scripts\run_demo.py
py -m unittest discover -s tests -v
py .\scripts\validate_config.py
py .\scripts\simulate_cache_regions.py
```

Optional local image conversion:

```powershell
py .\scripts\optimize_images.py --input .\sample-images --output .\optimized-images
```

Create `sample-images` and put local images inside it first. The optimizer never uploads files.

## Main files

- `lambda/index.js` — Lambda@Edge-compatible handler example for viewer-request and origin-response events.
- `edge_simulator.py` — local simulator for request filtering, WebP rewrites, headers, signed access, and synthetic regional cache stats.
- `configs/cloudfront-reference.json` — intended private-origin/OAC and signed-URL architecture.
- `configs/cache-policy.json` — example cache behavior.
- `scripts/` — demos, local config validation, cache-ratio simulation, and optional local image optimizer.
- `tests/` — automated tests using only Python's standard library.

## Design notes

### OAC and private S3
Keep S3 Block Public Access enabled and do not use an S3 website endpoint as the private origin. Configure CloudFront with an S3 REST origin and OAC signing (`sigv4`); the bucket policy should permit `s3:GetObject` only from the intended distribution. The reference JSON documents this but does not apply it.

### Lambda@Edge behavior
Lambda@Edge functions must be published as numbered versions in `us-east-1` and associated with supported CloudFront events. The included handler:
- blocks a small illustrative set of obviously suspicious query-string patterns;
- rewrites `.jpg`, `.jpeg`, or `.png` paths to sibling `.webp` paths only when `Accept` allows WebP;
- adds cache-control and security headers to origin responses.

The `.webp` object must already exist at the origin. The included local optimizer can create it before upload. True on-demand image transformation needs a suitable origin/compute design and can incur costs.

### Cache hit ratios
The regional script produces **synthetic** cache statistics using a deterministic sample workload. Real-world validation needs CloudFront logs/metrics and requests originating from multiple regions; this project intentionally does not do that.

### Signed URLs
For a real private behavior, configure CloudFront trusted key groups and use CloudFront's native signed URLs. Keep the private signing key only in a trusted server-side environment. Do not put private key material into this repository. The local simulator accepts an HMAC token solely to test expiry and tamper handling.

## Final local validation
- Python unit tests: 15 passed.
- JavaScript handler tests: 12 passed.
- Python and JavaScript syntax checks: passed.
- Configuration validator: passed.
- Local edge-behavior demo: passed.
- Synthetic regional cache simulation: passed.
- These results describe local tests only; no AWS deployment was performed.

## Repeat the JavaScript handler tests
```powershell
node --check .\lambda\index.js
node .\tests\test_lambda_edge.js
```

## Final status
The local reference implementation and automated tests are complete.
CloudFront, OAC, Lambda@Edge, CloudFront-native signed URLs, and real multi-region cache metrics remain undeployed or unverified.
