#!/bin/bash

sudo apt install -y postgresql
sudo systemctl start postgresql

sudo -u postgres psql <<EOF
CREATE DATABASE airflow_db;
CREATE USER airflow_user WITH PASSWORD 'airflow_pass';
ALTER DATABASE airflow_db OWNER TO airflow_user;
EOF
