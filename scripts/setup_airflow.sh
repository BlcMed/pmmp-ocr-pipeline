#!/bin/bash

export AIRFLOW_HOME=$pwd/airflow
echo "export AIRFLOW_HOME=${pwd}/airflow" >>venv/bin/activate
airflow users create --username user --firstname firstname --lastname lastname --role Admin --email admin@example.org
airflow db init
