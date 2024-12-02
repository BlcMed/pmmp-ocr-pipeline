import logging
import os

from dotenv import load_dotenv
from groq import Groq

from .config import load_config
from .data_manager import (
    load_miniO,
    save_postgresql,
    append_to_csv,
    save_dict_to_json,
)
from .llm_utils import extract_information_from_text

config = load_config("config.json")

log_file = os.path.join(config["LOG_FOLDER_PATH"], "info_extraction_pipeline.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
postgres_conn_id = "postgres_id"
table_name = "airflow_table"

textual_folder = config["TEXTUAL_FOLDER_PATH"]
extraction_fields = config["EXTRACTION_FIELDS"]
csv_file_path = config["CSV_FILE_PATH"]
json_folder_path = config["JSON_FOLDER_PATH"]
model_name = config["MODEL_NAME"]


def info_extraction_pipeline(
    textual_folder=textual_folder,
    extraction_fields=extraction_fields,
    api_key=groq_api_key,
    model_name=model_name,
    csv_file_path=csv_file_path,
    json_folder_path=json_folder_path,
):
    logging.info("Starting info extraction pipeline...")
    client = Groq(
        api_key=api_key,
    )
    textual_files = load_miniO(input_folder=textual_folder)
    logging.info(f"Found {len(textual_files)} files in {textual_folder}")
    for file_path in textual_files:
        if file_path.endswith(".txt"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                extracted_info = extract_information_from_text(
                    text, extraction_fields, client=client, model_name=model_name
                )
                save_dict_to_json(extracted_info, json_folder_path, file_path)
                append_to_csv(extracted_info, csv_file_path, file_path)
                save_postgresql(
                    data=extracted_info,
                    postgres_conn_id=postgres_conn_id,
                    table_name=table_name,
                )
                logging.info(f"Successfully processed and saved data from {file_path}")
            except Exception as e:
                logging.error(f"Error processing {file_path}: {e}")

    logging.info("Info extraction pipeline completed successfully.")


if __name__ == "__main__":

    from .config import load_config

    config = load_config("config.json")
    extraction_fields = config["EXTRACTION_FIELDS"]
    textual_folder = config["TEXTUAL_FOLDER_PATH"]
    csv_file_path = config["CSV_FILE_PATH"]
    json_folder_path = config["JSON_FOLDER_PATH"]
    model_name = config["MODEL_NAME"]

    info_extraction_pipeline(
        textual_folder=textual_folder,
        extraction_fields=extraction_fields,
        api_key=groq_api_key,
        model_name=model_name,
        csv_file_path=csv_file_path,
        json_folder_path=json_folder_path,
    )
