#!/bin/bash
set -e

echo "Creating thingsboard_db database if it does not exist..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    SELECT 'CREATE DATABASE thingsboard_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'thingsboard_db')\gexec
EOSQL
echo "thingsboard_db database creation script finished."

