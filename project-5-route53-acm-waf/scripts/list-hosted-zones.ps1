param([Parameter(Mandatory=$true)][string]$Region)
aws route53 list-hosted-zones --output table
