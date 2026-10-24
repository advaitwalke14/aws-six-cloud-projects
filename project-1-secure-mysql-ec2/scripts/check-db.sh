#!/usr/bin/env bash
set -euo pipefail
: "${DB_HOST:?Set DB_HOST}"
: "${DB_USER:?Set DB_USER}"
: "${DB_NAME:=secure_mysql_db}"
mysql --host="$DB_HOST" --user="$DB_USER" --password --database="$DB_NAME" \
  -e "SELECT VERSION(); SHOW TABLES; SELECT * FROM employees;"
