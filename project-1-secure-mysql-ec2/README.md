# Project 1 — Secure MySQL/MariaDB on EC2

## Current project scope

This repository currently contains:
- `sql/schema.sql` — creates `secure_mysql_db`, the `employees` table, and a demo row.
- `scripts/check-db.sh` — prompts for the DB password and checks the server version, tables, and sample rows.
- `sql/verify-tls.sql` — read-only SQL checks for TLS-related variables/session status.
- `docs/current-review.md` — sanitized findings from the read-only AWS review.
- `docs/free-completion-plan.md` — what can be completed without starting or changing AWS resources.
- `scripts/check-local-files.ps1` — checks that the local project files are present.

## Cost boundary

The current EC2 instance is stopped, but its attached EBS volume may still incur storage charges. This local review does not guarantee a zero AWS bill. No commands in the local checks create, start, stop, delete, or modify AWS resources.

## Run the local file check

From this folder in PowerShell:

```powershell
.\scripts\check-local-files.ps1
```

## TLS verification (only when a legitimate DB connection is available)

The SQL file `sql/verify-tls.sql` is read-only. Run it only after connecting to the intended database using the approved access path. Its output can vary by MySQL/MariaDB version. A configured TLS variable alone is not sufficient: verify that the client session has an active non-empty TLS cipher and that server policy requires secure transport where supported.

Do not start the stopped EC2 instance just to run a check until you have decided to accept any compute charges and confirmed how it will be reached securely.

## Known open items

Based on checks reported so far:
- The instance was stopped, had no public IPv4, and required IMDSv2.
- The attached 8 GiB gp3 volume was unencrypted.
- The security group showed SSH restricted to one `/32` source and no inbound TCP/3306 rule.
- No managed SSM instance or matching EBS snapshot was returned by the checks performed.
- Live database TLS enforcement, backup/restore, and encrypted EBS are not verified/completed.

Do not describe unverified items as completed. Enabling EBS encryption for an existing boot volume typically needs a copy/replacement workflow; do not attempt it casually because it can add cost and carries data risk.
## Verification status — cost-conscious mode
- Local required-file validation: PASS.
- Existing EC2 instance: STOPPED.
- Existing root EBS volume: 8 GiB, currently unencrypted.
- Existing snapshots for the root volume: none returned by the inspection.
- Live MySQL TLS verification: NOT COMPLETED.
- Database backup and restore verification: NOT COMPLETED.
- Disk encryption migration: NOT COMPLETED.
- No AWS resources were started or created during the read-only checks.
This project is locally documented but is not yet fully verified as a live, secure AWS deployment.
