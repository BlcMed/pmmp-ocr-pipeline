import os
import pandas as pd
from openai import OpenAI

SYSTEM_ROLE_CONTENT = 'You are an expert data extraction assistant. Your task is to read text documents and accurately extract specific information.'
api_key = ''

client = OpenAI(
    api_key=api_key
)

def extract_information_from_text(text, info_to_extract):
    # Create a dynamic prompt based on the info_to_extract list
    info_list_str = "\n".join([f"- {info}" for info in info_to_extract])
    output_format = ", ".join([f"{info}: <{info.replace(' ', '_').lower()}>" for info in info_to_extract])

    prompt = f"""
    Extract the following information from the text:
    {info_list_str}

    Text:
    {text}

    Output format: 
    {output_format}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_ROLE_CONTENT},
            {"role": "user", "content": prompt}
        ]
    )

    extracted_info = response.choices[0].message.content
    return extracted_info


def process_text_files(directory_path, info_to_extract):
    data = []
    
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                text = file.read()
                
            extracted_info = extract_information_from_text(text, info_to_extract)
            extracted_info["File"] = filename  # Add the filename to keep track of the source
            data.append(extracted_info)
    
    return pd.DataFrame(data)


if __name__ == '__main__':
    file_path = "./data_clone/textual/48-24.txt"
    info_to_extract = ["Objet de marché", "Maître d'ouvrage", "Journaux de publications", "Liste des concurrents", "Montant TTC"]
    with open(file_path, 'r') as file:
        text = file.read()
    extracted_info = extract_information_from_text(text, info_to_extract) 