# Advanced S3 Product Images

## Overview
Private S3 product-image storage with presigned URLs and local thumbnail generation.

## Current configuration
- AWS region: ap-south-1
- Bucket: product-images-809772106173-20261017
- Default encryption: SSE-S3 (AES256), verified previously
- S3 Block Public Access: all four settings enabled, verified previously
- Object Ownership: BucketOwnerEnforced, verified previously
- Lifecycle: temporary/ objects expire after 7 days, verified previously

## Requirements
```powershell
py -m pip install -r requirements.txt
```

## Generate a local thumbnail
```powershell
py .\app.py thumbnail E:\s3-product-images\product-source.jpg E:\s3-product-images\product-thumbnail-test.jpg
```

## Run automated tests
```powershell
py -m unittest discover -s tests -v
```

## Generate a presigned upload URL
```powershell
py .\app.py upload-url products/example.jpg --type image/jpeg
```

## Generate a presigned download URL
```powershell
py .\app.py download-url products/example.jpg
```

Presigned URL generation requires suitable AWS credentials. Generating a URL is not the same as uploading or downloading an object. Actual S3 requests can incur charges.

## Verified locally
- Python dependencies import successfully.
- Source JPEG was valid.
- Thumbnail output verified as JPEG, 200 x 150 pixels.
- All 10 automated tests passed.
- S3 presigned URL behavior was tested with mocks in the automated test suite.

## Previously verified AWS settings
- Bucket encryption defaults to AES256.
- All four S3 Block Public Access settings are enabled.
- Object Ownership is BucketOwnerEnforced.
- temporary/ objects expire after 7 days.
- No S3 Inventory configuration was found at the last inspection.

## Advanced requirements not yet deployed or verified
- CloudFront delivery for public product-image access.
- Cloud-based image transformation.
- Intelligent-Tiering and Glacier lifecycle transitions.
- S3 Inventory reports.
- Automated S3 upload malware scanning with Lambda and ClamAV.

## Security and cost notes
- Keep the bucket private; do not enable public access just to serve images.
- Do not commit AWS credentials or presigned URLs to source control.
- The ClamAV PowerShell script scans a local file only; it is not an automated S3 scanning pipeline.
- Configuration examples and local tests do not prove live AWS deployment.
- No additional AWS resources are created by the local test workflow.

## Completion status
Core S3 security settings and basic image utilities exist and have been partly verified. This project is not fully complete against all advanced requirements. CloudFront, cloud transformation, storage transitions, Inventory, and automated malware scanning remain pending live implementation or validated alternatives.

## Advanced reference examples - not deployed
- configs/lifecycle-advanced-reference.json: illustrative expiry and archive transitions.
- configs/s3-inventory-reference.json: inventory template with placeholder account and destination values.
- docs/cloudfront-private-s3-design.md: private S3 origin with CloudFront OAC.
- docs/malware-scanning-design.md: quarantine and scanning architecture.
These are local examples only. They have not been applied to the AWS account.
Inventory placeholders must be replaced and destination permissions configured before deployment.
Lifecycle transitions can incur charges if deployed; no such transition has been enabled by this workflow.
