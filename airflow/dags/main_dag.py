from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.scraping_pipeline import scraping_pipeline


def scraping():
    scraping_pipeline()
    print("start scraping ...")


def textualize():
    print("textualisation ...")


def info_extraction():
    print("info_extraction LLM ...")


def load_miniO():
    print("loading in miniO ...")


def save_miniO():
    print("saving in miniO ...")


def save_postgresql():
    print("saving in postgresql ...")


with DAG(
    dag_id="main_dag",
    schedule_interval="@daily",
    start_date=datetime(2024, 10, 1),
    catchup=False,
) as dag:

    task1 = PythonOperator(
        task_id="scraping_task",
        python_callable=scraping,
    )
    task2 = PythonOperator(task_id="staging_pdf_task", python_callable=save_miniO)

    task3 = PythonOperator(task_id="loading_pdf_task", python_callable=load_miniO)
    task4 = PythonOperator(
        task_id="textualize",
        python_callable=textualize,
    )
    task5 = PythonOperator(task_id="staging_text_task", python_callable=save_miniO)

    task6 = PythonOperator(task_id="loading_pdf_task", python_callable=load_miniO)
    task7 = PythonOperator(
        task_id="extract_information_with_llm",
        python_callable=info_extraction,
    )
    task8 = PythonOperator(
        task_id="sacing_structured_info", python_callable=save_postgresql
    )
