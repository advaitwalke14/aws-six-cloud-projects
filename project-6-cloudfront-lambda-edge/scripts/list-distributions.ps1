param([Parameter(Mandatory=$true)][string]$Region)
aws cloudfront list-distributions --region $Region --output table
