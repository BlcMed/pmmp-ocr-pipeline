import logging
import os
from typing import Any, Dict

from dotenv import load_dotenv
from groq import Groq

from .config import load_config
from .data_manager import append_to_csv, get_all_files, save_dict_to_json

config = load_config("config.json")

log_file = os.path.join(config["LOG_FOLDER_PATH"], "info_extraction_pipeline.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


def info_extraction_pipeline(
    textual_folder,
    extraction_fields,
    api_key,
    model_name,
    csv_file_path,
    json_folder_path,
):
    logging.info("Starting info extraction pipeline...")
    client = Groq(
        api_key=api_key,
    )
    textual_files_paths = get_all_files(input_folder=textual_folder)
    logging.info(f"Found {len(textual_files_paths)} files in {textual_folder}")
    for file_path in textual_files_paths:
        if file_path.endswith(".txt"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                extracted_info = extract_information_from_text(
                    text, extraction_fields, client=client, model_name=model_name
                )
                save_dict_to_json(extracted_info, json_folder_path, file_path)
                append_to_csv(extracted_info, csv_file_path, file_path)
                logging.info(f"Successfully processed and saved data from {file_path}")
            except Exception as e:
                logging.error(f"Error processing {file_path}: {e}")

    logging.info("Info extraction pipeline completed successfully.")


def extract_information_from_text(
    text: str, extraction_fields: list[str], client, model_name
) -> Dict[str, Any]:
    """
    Extract specified information from a text file using OpenAI's language model.

    Returns:
    - dict: A dictionary with the extracted information.
    """
    prompt = generate_prompt(extraction_fields=extraction_fields, text=text)

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        completion_text = response.choices[0].message.content.strip()
        logging.debug(f"Completion text: {completion_text}")
        results = _parse_completion_to_dict(completion_text, extraction_fields)
        logging.info("Information extracted successfully.")
        return results
    except Exception as e:
        logging.error(f"Failed to extract information: {e}")
        raise


def generate_prompt(extraction_fields: list[str], text: str) -> str:
    """
    Create a dynamic prompt based on the extraction_fields
    """
    info_list_str = "\n".join([f"- {info}" for info in extraction_fields])
    output_format = ", ".join(
        [f"{info}: <{info.replace(' ', '_').lower()}>" for info in extraction_fields]
    )

    prompt = f"""
    Extract the following information:
    {info_list_str}

    Be as concise as possible and the output format should be:
    {output_format}

    from the text:
    {text}

    """
    logging.debug(f"Generated prompt: {prompt}")
    return prompt


def _parse_completion_to_dict(completion_text, extraction_fields):
    logging.info("Parsing completion text into a dictionary...")
    result = {}
    for field in extraction_fields:
        key = field.lower().replace(" ", "_")
        # Look for the field in the completion text
        start = completion_text.find(f"{field}:")
        if start != -1:
            start += len(f"{field}:")
            end = completion_text.find(",", start)
            result[key] = completion_text[start:end].strip()
        else:
            result[key] = None
    logging.debug(f"Parsed result: {result}")
    return result


if __name__ == "__main__":

    from .config import load_config

    config = load_config("config.json")
    extraction_fields = config["EXTRACTION_FIELDS_PATH"]
    textual_folder = config["TEXTUAL_FOLDER_PATH"]
    csv_file_path = config["CSV_FILE_PATH"]
    json_folder_path = config["JSON_FOLDER_PATH"]
    model_name = config["MODEL_NAME"]
    # file_path = "./data/textual/48-24.txt"
    # client = Groq(api_key=groq_api_key)
    # extracted_info = extract_information_from_text(text, extraction_fields, client=client)
    # append_to_csv(extracted_info=extracted_info, csv_file_path= csv_file_path,file_path=file_path)

    info_extraction_pipeline(
        textual_folder=textual_folder,
        extraction_fields=extraction_fields,
        api_key=groq_api_key,
        model_name=model_name,
        csv_file_path=csv_file_path,
        json_folder_path=json_folder_path,
    )
