# Read-only inventory only. Does not create or modify AWS resources.
$ErrorActionPreference = "Continue"
Write-Host "Route 53 hosted zones (may show empty output):"
aws route53 list-hosted-zones --query "HostedZones[].{Name:Name,Id:Id,Private:Config.PrivateZone}" --output table
Write-Host "`nACM certificates for CloudFront (us-east-1):"
aws acm list-certificates --region us-east-1 --output table
Write-Host "`nACM certificates for an example regional ALB (ap-south-1):"
aws acm list-certificates --region ap-south-1 --output table
Write-Host "`nRegional WAF web ACLs (ap-south-1):"
aws wafv2 list-web-acls --scope REGIONAL --region ap-south-1 --output table
Write-Host "`nCloudFront-scope WAF web ACLs (us-east-1):"
aws wafv2 list-web-acls --scope CLOUDFRONT --region us-east-1 --output table
Write-Host "`nRead-only checks complete. No resources were created."
