param([Parameter(Mandatory=$true)][string]$Region)
aws acm list-certificates --region $Region --output table
