-- Create the database
CREATE DATABASE airflow_db;

-- Create the user with a password
CREATE USER airflow_user WITH PASSWORD 'airflow_pass';

-- Grant ownership of the database to the user
ALTER DATABASE airflow_db OWNER TO airflow_user;
