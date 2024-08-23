from textify_docs.document_converter import DocumentConverter
from .data_manager import *

SUPPORTED_FILE_FORMATS=['docx','.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.xls', '.xlsx']
COMPRESSED_FILE_FORMATS = ['.zip']

def main_pipeline(
    input_folder,
    extracted_zips_folder,
    textual_folder,
):
    input_files = get_all_files(input_folder=input_folder)
    document_converter = DocumentConverter()

    core_pipeline(input_folder=input_folder, output_folder=textual_folder, document_converter=document_converter)
    zip_input_files = [input_file for input_file in input_files if get_file_extention(input_file) in COMPRESSED_FILE_FORMATS]
    for input_file in zip_input_files:
        extract_zip(input_file, extracted_zips_folder)
    core_pipeline(input_folder=extracted_zips_folder, output_folder=textual_folder, document_converter=document_converter)



def core_pipeline(
    input_folder,
    output_folder,
    document_converter
):
    input_files = get_all_files(input_folder=input_folder)

    for input_file in input_files:
        file_extention = get_file_extention(input_file)
        if file_extention in SUPPORTED_FILE_FORMATS:
            text = document_converter.convert_to_text(input_file)
            print(text)
            save_text_to_file(text, output_folder=output_folder, input_path=input_file)
 
if __name__ == '__main__':

    # Define paths
    base_data_path = './data_clone/'
    raw_data_path = base_data_path + 'raw/'
    files_source_path = raw_data_path + 'scrapped_documents/'
    extracted_zips_folder = raw_data_path + 'extracted_zips/'
    input_folder = files_source_path
    textual_folder = base_data_path + 'textual/'

    main_pipeline(input_folder = input_folder,
            extracted_zips_folder=extracted_zips_folder,
            textual_folder=textual_folder)
