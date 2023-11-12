#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

create user $USER with password '$PASSWORD';
create database $DATABASE with owner=$USER;
GRANT ALL PRIVILEGES ON DATABASE $DATABASE TO $USER;
EOSQL