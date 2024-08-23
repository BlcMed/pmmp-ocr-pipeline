import os
import zipfile

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


def extract_zip(self, zip_path, extract_to):
    """
    Extract a ZIP file to a specified directory.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
