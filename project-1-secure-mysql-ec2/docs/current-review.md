# Project 1 — Sanitized current review

This file records only the read-only results reported during the current review. Account-specific IDs, IP addresses, key-pair names, and other unique identifiers are intentionally omitted.

## Verified observations

- EC2 instance type: `t3.micro`; state: `stopped`.
- No public IPv4 address was assigned.
- Private IPv4 address existed in a VPC using the `10.0.0.0/16` range.
- IMDSv2 tokens were required.
- No IAM instance profile was attached.
- The shown security group allowed SSH from one single-host `/32` source.
- No inbound TCP port `3306` rule was shown in that security group.
- Attached volume: 8 GiB `gp3`, encrypted: `false`, delete-on-termination: `true`.
- No matching snapshot was returned for the current volume ID.
- SSM instance-information query returned no row for the instance.
- VPC routing inspected so far did not show an internet route for the `10.0.0.0/16` VPC route table. A separate S3 gateway endpoint was available.

## Not proven by the above

- That the MariaDB server is currently running or reachable (instance is stopped).
- That TLS is enabled or enforced.
- That backups or point-in-time restore work.
- That EBS data is encrypted.
- That the database is protected from every network path. Continue reviewing route tables, NACLs, and all attached security groups before making broader claims.

## Cost/data cautions

- EBS storage may incur charges while the instance is stopped.
- The boot volume has delete-on-termination enabled. Do not terminate the instance unless data loss is explicitly intended and a verified backup exists.
- Do not expose TCP/3306 to `0.0.0.0/0`.
- Do not commit private keys or credentials into a repository.
