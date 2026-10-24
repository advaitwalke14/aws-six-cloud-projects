-- Read-only diagnostic queries for a MySQL/MariaDB session.
-- Run only after securely connecting to the intended database.
-- Results vary by engine/version. A variable value alone is not proof of
-- an encrypted connection; check the current session's Ssl_cipher as well.

SELECT VERSION() AS database_version;

SHOW GLOBAL VARIABLES LIKE 'have_ssl';
SHOW GLOBAL VARIABLES LIKE 'tls_version';
SHOW GLOBAL VARIABLES LIKE 'require_secure_transport';

SHOW SESSION STATUS LIKE 'Ssl_cipher';
SHOW SESSION STATUS LIKE 'Ssl_version';
