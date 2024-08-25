from textify_docs.document_converter import DocumentConverter
from .data_manager import *


def main_pipeline(
    input_folder,
    extracted_zips_folder,
    textual_folder,
    supported_file_formats,
    compressed_file_formats
):
    input_files = get_all_files(input_folder=input_folder)
    document_converter = DocumentConverter()

    core_pipeline(input_folder=input_folder, output_folder=textual_folder, document_converter=document_converter, supported_file_formats=supported_file_formats)
    zip_input_files = [input_file for input_file in input_files if get_file_extention(input_file) in compressed_file_formats]
    for input_file in zip_input_files:
        extract_zip(zip_path=input_file, extract_to=extracted_zips_folder)
    #core_pipeline(input_folder=extracted_zips_folder, output_folder=textual_folder, document_converter=document_converter)


def core_pipeline(
    input_folder,
    output_folder,
    document_converter,
    supported_file_formats
):
    input_files = get_all_files(input_folder=input_folder)

    for input_file in input_files:
        file_extention = get_file_extention(input_file)
        if file_extention in supported_file_formats:
            text = document_converter.convert_to_text(input_file)
            print(text)
            save_text_to_file(text, output_folder=output_folder, input_path=input_file)
 
if __name__ == '__main__':

    from .config import load_config
    config = load_config('config.json')
    input_folder = config["INPUT_FOLDER"]
    extracted_zips_folder = config["EXTRACTED_ZIPS_FOLDER"]
    textual_folder = config["TEXTUAL_FOLDER"]
    supported_file_formats = config["SUPPORTED_FILE_FORMATS"]
    compressed_file_formats = config["COMPRESSED_FILE_FORMATS"]

    main_pipeline(input_folder = input_folder,
            extracted_zips_folder=extracted_zips_folder,
            textual_folder=textual_folder,
            supported_file_formats=supported_file_formats,
            compressed_file_formats=compressed_file_formats
            )
