# Private S3 + CloudFront reference design
Status: Documentation only; not deployed.
1. Keep the product-image S3 bucket private.
2. Configure a CloudFront distribution with the S3 bucket as its origin.
3. Use Origin Access Control (OAC) with signed origin requests.
4. Grant the specific CloudFront distribution permission to read approved
   objects through the S3 bucket policy.
5. Keep all S3 Block Public Access settings enabled.
6. Test that the CloudFront URL works and direct anonymous S3 URLs remain
   denied.
7. Review HTTPS, cache policy, error responses, and invalidation behavior.
Do not create a distribution or edit the live bucket policy as part of the
free-only workflow. CloudFront usage may incur charges.
