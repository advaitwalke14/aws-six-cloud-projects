# Project 6 architecture

```text
Viewer
  |
  | HTTPS + optional CloudFront-native signed URL
  v
CloudFront Distribution
  |-- trusted key group validates signed URL for private behavior
  |-- Lambda@Edge viewer-request:
  |      reject suspicious query strings
  |      rewrite accepted JPEG/PNG request to pre-generated WebP object
  |
  |-- Origin Access Control (SigV4)
  v
Private S3 REST origin (Block Public Access enabled)

Origin response
  `-- Lambda@Edge origin-response adds Cache-Control/security headers
```

## Real AWS deployment notes (not executed)

- CloudFront must use a private S3 REST origin with OAC; do not make the bucket public.
- The bucket policy should limit `s3:GetObject` to the intended CloudFront distribution.
- Lambda@Edge functions are created in `us-east-1`, published as numbered versions, and associated to CloudFront events.
- CloudFront signed URLs use trusted key groups/public keys and CloudFront's native signature format. The local HMAC simulator is not interchangeable with native signing.
- The origin must already contain each `.webp` variant. The local optimizer creates variants offline.
- Cache hit ratio across actual regions must be measured with real CloudFront metrics/logs and remote traffic. The included regional cache script is synthetic only.
- This project has intentionally not deployed or validated any real AWS resource because the stated target is no new AWS spend.
