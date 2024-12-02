from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.scraping_pipeline import scrape_documents
from src.info_extraction_pipeline import info_extraction_pipeline
from src.ocr_pipeline import textualize
import os
from dotenv import load_dotenv

from src.config import load_config

config = load_config("config.json")

extraction_fields = config["EXTRACTION_FIELDS"]
json_folder_path = config["JSON_FOLDER_PATH"]
model_name = config["MODEL_NAME"]
input_folder = config["INPUT_FOLDER_PATH"]
extracted_zips_folder = config["EXTRACTED_ZIPS_FOLDER_PATH"]
textual_folder = config["TEXTUAL_FOLDER_PATH"]
csv_file_path = config["CSV_FILE_PATH"]
supported_file_formats = config["SUPPORTED_FILE_FORMATS"]
compressed_file_formats = config["COMPRESSED_FILE_FORMATS"]


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


with DAG(
    dag_id="main_dag",
    schedule_interval="@daily",
    start_date=datetime(2024, 10, 1),
    catchup=False,
) as dag:

    task1 = PythonOperator(
        task_id="scraping_task",
        python_callable=scrape_documents,
    )

    task2 = PythonOperator(
        task_id="textualize_task",
        python_callable=textualize,
    )

    task3 = PythonOperator(
        task_id="extract_information_with_llm",
        python_callable=info_extraction_pipeline,
    )

    task1 >> task2 >> task3
