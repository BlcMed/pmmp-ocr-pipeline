import os
import csv
import zipfile


def append_to_csv(extracted_info, csv_file_path, file_path):
    """
    Appends extracted information to an existing CSV file, including the file name as a column.

    Args:
        extracted_info (dict): A dictionary containing the extracted information.
        csv_file_path (str): The path to the existing CSV file.
        file_name (str): The name of the file from which the information was extracted.
    """

    # Add the file path to the extracted information
    extracted_info['file_path'] = file_path

    # Check if the file exists to determine whether to write headers
    file_exists = os.path.isfile(csv_file_path)
    # Extract keys for CSV headers
    headers = extracted_info.keys()

    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        # Write header if the file does not exist
        if not file_exists:
            writer.writeheader()
        # Write the row
        writer.writerow(extracted_info)

def get_all_files(input_folder):
    """
    get all file names in a folder
    """
    file_paths = []
    for root, dirs, files in os.walk(input_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_paths.append(file_path)
    return file_paths

def get_file_extention(input_path):
    filename, file_extension = os.path.splitext(input_path)
    file_extension = file_extension.lower()
    return file_extension

def save_text_to_file(text, output_folder,input_path):
        """
        Save text to a file in the specified folder.
        """
        filename = os.path.splitext(input_path)[0]
        base_filename = os.path.basename(filename)
        output_path = os.path.join(output_folder, f"{base_filename}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)


def extract_zip(zip_path, extract_to):
    """
    Extract a ZIP file to a specified directory.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


if __name__ == '__main__':
    extracted_info = {
        "Objet de marché": "alfkj",
        "Maître d'ouvrage": "sdfasdf",
        "Journaux de publications": "sdfda sadf",
        "Liste des concurrents": "X, Y",
        "Montant TTC": "1,200,000 dh"
    }
    csv_file_path = './data_clone/extracted_info.csv'
    file_path = "data/file_example.text"
    append_to_csv(extracted_info, csv_file_path,file_path = file_path)