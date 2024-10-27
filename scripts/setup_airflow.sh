#! /bin/bash

pip install apache-airflow==2.10.2
export AIRFLOW_HOME=$pwd/airflow
echo "export AIRFLOW_HOME=${pwd}/airflow" >>venv/bin/activate
airflow db init
airflow users create --username user --firstname firstname --lastname lastname --role Admin --email admin@example.org