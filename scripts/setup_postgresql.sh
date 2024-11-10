#!/bin/bash

# Install PostgreSQL and start it
sudo apt install -y postgresql
sudo systemctl start postgresql
sudo systemctl enable postgresql

SQL_FILE="./setup_airflow_db.sql"
if [ ! -f "$SQL_FILE" ]; then
    echo "Error: SQL file '$SQL_FILE' not found."
    exit 1
fi

echo "Running SQL script to set up the database and user..."
sudo -u postgres psql -f "$SQL_FILE"

echo "PostgreSQL database and user for Airflow have been created successfully."
