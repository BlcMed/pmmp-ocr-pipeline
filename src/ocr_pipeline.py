import logging
import os

from textify_docs.document_converter import DocumentConverter

from .config import load_config
from .data_manager import (
    _get_file_extention,
    extract_zip,
    get_all_files,
    save_text_to_file,
)

config = load_config("config.json")

log_file = os.path.join(config["LOG_FOLDER_PATH"], "ocr_pipeline.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)


def main_OCR_pipeline(
    input_folder,
    extracted_zips_folder,
    textual_folder,
    supported_file_formats,
    compressed_file_formats,
):
    logging.info("Starting main OCR pipeline...")
    input_files = get_all_files(input_folder=input_folder)
    document_converter = DocumentConverter()

    logging.info(f"Processing files in {input_folder}")
    core_OCR_pipeline(
        input_folder=input_folder,
        output_folder=textual_folder,
        document_converter=document_converter,
        supported_file_formats=supported_file_formats,
    )
    zip_input_files = [
        input_file
        for input_file in input_files
        if _get_file_extention(input_file) in compressed_file_formats
    ]
    logging.info(f"Found {len(zip_input_files)} compressed files to extract.")
    for input_file in zip_input_files:
        logging.info(f"Extracting {input_file}...")
        extract_zip(zip_path=input_file, extract_to=extracted_zips_folder)

    logging.info(f"Processing extracted files in {extracted_zips_folder}")
    core_OCR_pipeline(
        input_folder=extracted_zips_folder,
        output_folder=textual_folder,
        document_converter=document_converter,
    )
    logging.info("Main pipeline completed successfully.")


def core_OCR_pipeline(
    input_folder, output_folder, document_converter, supported_file_formats
):
    input_files = get_all_files(input_folder=input_folder)
    logging.info(f"Found {len(input_files)} files in {input_folder}")

    for input_file in input_files:
        file_extention = _get_file_extention(input_file)
        if file_extention in supported_file_formats:
            logging.info(f"Converting {input_file} to text...")
            try:
                text = document_converter.convert_to_text(input_file)
                save_text_to_file(
                    text, output_folder=output_folder, input_path=input_file
                )
                logging.info(f"Successfully processed {input_file}")
            except Exception as e:
                logging.error(f"Failed to process {input_file}: {e}")


if __name__ == "__main__":

    from .config import load_config

    config = load_config("config.json")
    input_folder = config["INPUT_FOLDER_PATH"]
    extracted_zips_folder = config["EXTRACTED_ZIPS_FOLDER_PATH"]
    textual_folder = config["TEXTUAL_FOLDER_PATH"]
    supported_file_formats = config["SUPPORTED_FILE_FORMATS"]
    compressed_file_formats = config["COMPRESSED_FILE_FORMATS"]

    main_OCR_pipeline(
        input_folder=input_folder,
        extracted_zips_folder=extracted_zips_folder,
        textual_folder=textual_folder,
        supported_file_formats=supported_file_formats,
        compressed_file_formats=compressed_file_formats,
    )
