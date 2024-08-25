import os
import pandas as pd
from openai import OpenAI
from .data_manager import append_to_csv
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
#SYSTEM_ROLE_CONTENT = 'You are an expert data extraction assistant. Your task is to read text documents and accurately extract specific information.'
#CSV_FILE_PATH = './data_clone/extracted_info.csv'
client = OpenAI(api_key=api_key)

def extract_information_from_text(text, extraction_fields, system_role_content):
    # Create a dynamic prompt based on the extraction_fields
    info_list_str = "\n".join([f"- {info}" for info in extraction_fields])
    output_format = ", ".join([f"{info}: <{info.replace(' ', '_').lower()}>" for info in extraction_fields])

    prompt = f"""
    Extract the following information from the text:
    {info_list_str}

    Text:
    {text}

    Output format: 
    {output_format}
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_role_content},
            {"role": "user", "content": prompt}
        ]
    )

    completion_text = response.choices[0].message.content.strip()
    return _parse_completion_to_dict(completion_text, extraction_fields)


def _parse_completion_to_dict(completion_text, extraction_fields):
    result = {}
    for field in extraction_fields:
        key = field.lower().replace(' ', '_')
        # Look for the field in the completion text
        start = completion_text.find(f"{field}:")
        if start != -1:
            start += len(f"{field}:")
            end = completion_text.find(",", start)
            result[key] = completion_text[start:end].strip()
        else:
            result[key] = None
    return result


if __name__ == '__main__':
    file_path = "./data_clone/textual/48-24.txt"
    # extraction_fields = ["Objet de marché", "Maître d'ouvrage", "Journaux de publications", "Liste des concurrents", "Montant TTC"]
    from .config import load_config
    config = load_config('config.json')
    extraction_fields = config["EXTRACTION_FIELDS"]
    csv_file_path = config["CSV_FILE_PATH"]

    with open(file_path, 'r') as file:
        text = file.read()
    extracted_info = extract_information_from_text(text, extraction_fields) 

    append_to_csv(extracted_info=extracted_info, csv_file_path= csv_file_path,file_path=file_path)