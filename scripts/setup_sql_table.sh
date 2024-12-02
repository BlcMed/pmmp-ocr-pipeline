#!/bin/bash

DB_NAME="airflow_db"
USER="airflow_user"
SQL_FILE_PATH="./scripts/create_table.sql"

DB_EXISTS=$(sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'")
if [[ $DB_EXISTS != "1" ]]; then
    echo "Database '$DB_NAME' does not exist. Please run 'setup_postgresql.sh' first."
    exit 1
fi

if [ ! -f "$SQL_FILE_PATH" ]; then
    echo "Error: SQL file '$SQL_FILE_PATH' not found."
    exit 1
fi

echo "Executing SQL file '$SQL_FILE_PATH' on database '$DB_NAME'..."

cat $SQL_FILE_PATH

export PGPASSWORD='airflow_pass'
sudo -u postgres psql -d "$DB_NAME" -U "$DB_USER" -f "$SQL_FILE_PATH"

if [ $? -eq 0 ]; then
    echo "SQL file executed successfully."
else
    echo "Failed to execute SQL file."
    exit 1
fi
