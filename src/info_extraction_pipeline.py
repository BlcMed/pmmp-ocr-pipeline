import os
from openai import OpenAI
from .data_manager import append_to_csv, get_all_files


def info_extraction_pipeline(textual_folder, extraction_fields, csv_file_path, api_key, system_role_content):
    client = load_openai_client(api_key=api_key)
    textual_files_paths = get_all_files(input_folder=textual_folder)
    for file_path in textual_files_paths:
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            extracted_info = extract_information_from_text(text, extraction_fields, system_role_content, client=client)
            append_to_csv(extracted_info, csv_file_path, file_path)

def load_openai_client(api_key):
    client = OpenAI(api_key=api_key)
    return client

def extract_information_from_text(text, extraction_fields, system_role_content, client):
    """
    Extract specified information from a text file using OpenAI's language model.

    Args:
    - text (str): The textual data.
    - extraction_fields (list): A list of strings representing the information to extract.

    Returns:
    - dict: A dictionary with the extracted information.
    """
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
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    client = load_openai_client(api_key=api_key)

    file_path = "./data_clone/textual/48-24.txt"

    from .config import load_config
    config = load_config('config.json')
    extraction_fields = config["EXTRACTION_FIELDS"]
    textual_folder = config["TEXTUAL_FOLDER"]
    csv_file_path = config["CSV_FILE_PATH"]
    system_role_content = config["SYSTEM_ROLE_CONTENT"]


    info_extraction_pipeline(textual_folder=textual_folder,extraction_fields=extraction_fields,csv_file_path=csv_file_path,api_key=api_key,system_role_content=system_role_content)
    #with open(file_path, 'r') as file:
    #    text = file.read()
    #extracted_info = extract_information_from_text(text, extraction_fields, client=client) 

    #append_to_csv(extracted_info=extracted_info, csv_file_path= csv_file_path,file_path=file_path)