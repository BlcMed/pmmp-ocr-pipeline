import logging
import os

from textify_docs.document_converter import DocumentConverter

from .config import load_config
from .data_manager import (
    get_file_extention,
    get_file_name,
    load_miniO,
    save_miniO,
    # extract_zip,
    # save_text_to_file,
)

config = load_config("config.json")

log_file = os.path.join(config["LOG_FOLDER_PATH"], "ocr_pipeline.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)
input_folder = config["INPUT_FOLDER_PATH"]
textual_folder = config["TEXTUAL_FOLDER_PATH"]
supported_file_formats = config["SUPPORTED_FILE_FORMATS"]


def textualize(input_folder=input_folder, textual_folder=textual_folder):
    logging.info("Starting tetualization ...")
    input_files = load_miniO(input_folder=input_folder)
    document_converter = DocumentConverter()
    for input_file in input_files:
        file_extention = get_file_extention(input_file)
        if file_extention in supported_file_formats:
            logging.info(f"Converting {input_file} to text...")
            text = document_converter.convert_to_text(input_file)
            try:
                text = document_converter.convert_to_text(input_file)
                base_filename = get_file_name(input_file) + ".txt"
                logging.info(f"Successfully processed {input_file}")
            except Exception as e:
                logging.error(f"Failed to process {input_file}: {e}")
            save_miniO(content=text, path=textual_folder, object_name=base_filename)


if __name__ == "__main__":

    from .config import load_config

    config = load_config("config.json")
    input_folder = config["INPUT_FOLDER_PATH"]
    extracted_zips_folder = config["EXTRACTED_ZIPS_FOLDER_PATH"]
    textual_folder = config["TEXTUAL_FOLDER_PATH"]
    supported_file_formats = config["SUPPORTED_FILE_FORMATS"]
    compressed_file_formats = config["COMPRESSED_FILE_FORMATS"]
    textualize(input_folder=input_folder, textual_folder=textual_folder)
