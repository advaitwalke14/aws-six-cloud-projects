param([Parameter(Mandatory=$true)][string]$Region)
aws cloudwatch describe-alarms --region $Region --output table
