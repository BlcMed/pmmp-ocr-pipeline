import os
from typing import Any, Dict

from dotenv import load_dotenv
from groq import Groq

from .data_manager import append_to_csv, get_all_files, save_dict_to_json

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


def info_extraction_pipeline(
    textual_folder, extraction_fields, api_key, csv_file_path, json_folder_path
):
    client = Groq(
        api_key=api_key,
    )
    textual_files_paths = get_all_files(input_folder=textual_folder)
    for file_path in textual_files_paths:
        if file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            extracted_info = extract_information_from_text(
                text, extraction_fields, client=client
            )
            save_dict_to_json(extracted_info, json_folder_path, file_path)
            append_to_csv(extracted_info, csv_file_path, file_path)


def extract_information_from_text(
    text: str, extraction_fields: list[str], client
) -> Dict[str, Any]:
    """
    Extract specified information from a text file using OpenAI's language model.

    Returns:
    - dict: A dictionary with the extracted information.
    """
    prompt = generate_prompt(extraction_fields=extraction_fields, text=text)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    completion_text = response.choices[0].message.content.strip()
    # print(f"completion_text: {completion_text}")
    results = _parse_completion_to_dict(completion_text, extraction_fields)
    # print(f"rsults: {results}")
    return results


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
    return prompt


def _parse_completion_to_dict(completion_text, extraction_fields):
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
    return result


if __name__ == "__main__":

    from .config import load_config

    config = load_config("config.json")
    extraction_fields = config["EXTRACTION_FIELDS"]
    textual_folder = config["TEXTUAL_FOLDER"]
    csv_file_path = config["CSV_FILE_PATH"]
    json_folder_path = config["JSON_FOLDER_PATH"]
    # file_path = "./data/textual/48-24.txt"
    # client = Groq(api_key=groq_api_key)
    # extracted_info = extract_information_from_text(text, extraction_fields, client=client)
    # append_to_csv(extracted_info=extracted_info, csv_file_path= csv_file_path,file_path=file_path)

    info_extraction_pipeline(
        textual_folder=textual_folder,
        extraction_fields=extraction_fields,
        api_key=groq_api_key,
        csv_file_path=csv_file_path,
        json_folder_path=json_folder_path,
    )
