# Free-first completion plan

## Can be done locally without new AWS resources
- Keep schema and connection scripts organized and documented.
- Review the SQL checks and create a TLS verification query for later.
- Prepare a backup/restore runbook with commands but do not claim it was tested.
- Run local file-integrity checks and document known gaps.
- Prepare a sanitized project README.

## Requires live access or resource/configuration changes
- Confirm actual TLS cipher for a live database client session.
- Enforce `require_secure_transport` (or the supported equivalent) and verify clients use TLS.
- Run an actual database backup and restore test.
- Encrypt the existing root EBS volume. This is not a simple toggle for an existing root volume; use an approved snapshot/copy/replacement procedure with a verified rollback plan. This can incur AWS charges.
- Verify all effective network rules and routes in the running environment.

## Recommended order
1. Keep EC2 stopped until a cost and access decision is made.
2. Complete local documentation and run `scripts/check-local-files.ps1`.
3. If live verification is later approved, estimate any costs first and establish secure access.
4. Verify TLS and backup/restore.
5. Handle EBS encryption only after planning a safe replacement/rollback and understanding potential charges.

This plan intentionally does not create, start, stop, or modify AWS resources.
