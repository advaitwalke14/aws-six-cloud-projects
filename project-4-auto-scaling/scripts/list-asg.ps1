param([Parameter(Mandatory=$true)][string]$Region)
aws autoscaling describe-auto-scaling-groups --region $Region --output table
