from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.scraping_pipeline import scraping_pipeline
from airflow.decorators import task_group


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

    @task_group(group_id="scraping_task_group")
    def scraping_task():
        task1 = PythonOperator(
            task_id="scraping_task",
            python_callable=scraping,
        )
        task2 = PythonOperator(task_id="staging_pdf_task", python_callable=save_miniO)

        task1 >> task2

    @task_group(group_id="textualization_task_group")
    def textualization():
        task3 = PythonOperator(task_id="loading_pdf_task", python_callable=load_miniO)
        task4 = PythonOperator(
            task_id="textualize",
            python_callable=textualize,
        )
        task5 = PythonOperator(task_id="staging_text_task", python_callable=save_miniO)

        task3 >> task4 >> task5

    @task_group(group_id="info_extraction_task_group")
    def information_extraction():
        task6 = PythonOperator(task_id="loading_pdf_task", python_callable=load_miniO)
        task7 = PythonOperator(
            task_id="extract_information_with_llm",
            python_callable=info_extraction,
        )
        task8 = PythonOperator(
            task_id="sacing_structured_info", python_callable=save_postgresql
        )

        task6 >> task7 >> task8

    scraping_task() >> textualization() >> information_extraction()
