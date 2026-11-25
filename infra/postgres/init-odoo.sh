#!/bin/sh
# Runs once, on an empty data volume: dedicated role for Odoo (Odoo refuses the superuser).
set -e
psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
  -c "CREATE ROLE odoo LOGIN CREATEDB PASSWORD '$ODOO_DB_PASSWORD';"
