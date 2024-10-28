import csv
import json
import logging
import os
import zipfile

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def save_dict_to_json(data: dict, json_folder_path, file_path: str):
    """
    Saves a dictionary to a JSON file.
    """
    file_name = _get_file_name(file_path)
    json_file_path = os.path.join(json_folder_path, file_name + ".json")

    try:
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        logging.info("Dictionary saved to %s", json_file_path)
    except Exception as e:
        logging.error(f"Error saving to JSON: {e}")


def append_to_csv(extracted_info, csv_file_path: str, file_path: str):
    """
    Appends extracted information to an existing CSV file, including the file name as a column.

    Args:
        extracted_info (dict): A dictionary containing the extracted information.
    """

    # Add the file path to the extracted information
    extracted_info["file_path"] = file_path

    # Check if the file exists to determine whether to write headers
    file_exists = os.path.isfile(csv_file_path)
    # Extract keys for CSV headers
    headers = extracted_info.keys()

    try:
        with open(csv_file_path, mode="a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            writer.writerow(extracted_info)
        logging.info(f"Appended extracted info from {file_path} to {csv_file_path}")
    except Exception as e:
        logging.error(f"Error writing to CSV: {e}")


def get_all_files(input_folder):
    """
    Get all file names in a folder
    """
    file_paths = []
    for root, dirs, files in os.walk(input_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_paths.append(file_path)
    return file_paths


def get_file_extention(input_path: str) -> str:
    _, file_extension = os.path.splitext(input_path)
    file_extension = file_extension.lower()
    return file_extension


def _get_file_name(file_path: str) -> str:
    """
    Get the base name (without extension) of a file.
    """
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    return file_name


def save_text_to_file(text: str, output_folder: str, input_path: str):
    """
    Save text to a file in the specified folder.
    """
    try:
        base_filename = _get_file_name(input_path)
        output_path = os.path.join(output_folder, f"{base_filename}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"Error saving text to file: {e}")

        logging.info(f"Text saved to {output_path}")
    except Exception as e:
        logging.error(f"Error saving text to file: {e}")


def extract_zip(zip_path, extract_to):
    """
    Extract a ZIP file to a specified directory.
    """
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        logging.info(f"Extracted {zip_path} to {extract_to}")
    except Exception as e:
        logging.error(f"Error extracting zip file {zip_path}: {e}")


if __name__ == "__main__":
    extracted_info = {
        "Objet de marché": "alfkj",
        "Maître d'ouvrage": "sdfasdf",
        "Journaux de publications": "sdfda sadf",
        "Liste des concurrents": "X, Y",
        "Montant TTC": "1,200,000 dh",
    }
    csv_file_path = "./data/extracted_info_test.csv"
    file_path = "root_test/test/test_file.txt"

    # append_to_csv(extracted_info, csv_file_path, file_path=file_path)
    save_dict_to_json(extracted_info, "./data/", file_path)
