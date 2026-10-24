param([Parameter(Mandatory=$true)][string]$Region)
aws wafv2 list-web-acls --scope REGIONAL --region $Region --output table
