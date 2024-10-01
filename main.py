import os

from dotenv import load_dotenv

from src.config import load_config
from src.info_extraction_pipeline import info_extraction_pipeline
from src.ocr_pipeline import main_OCR_pipeline
from src.scraping_pipeline import scraping_pipeline


def main():
    # Load configuration
    config = load_config("config.json")
    input_folder = config["INPUT_FOLDER"]
    extracted_zips_folder = config["EXTRACTED_ZIPS_FOLDER"]
    textual_folder = config["TEXTUAL_FOLDER"]
    supported_file_formats = config["SUPPORTED_FILE_FORMATS"]
    compressed_file_formats = config["COMPRESSED_FILE_FORMATS"]
    # os.makedirs(extracted_zips_folder, exist_ok=True)
    scraping_pipeline()
    main_OCR_pipeline(
        input_folder=input_folder,
        extracted_zips_folder=extracted_zips_folder,
        textual_folder=textual_folder,
        supported_file_formats=supported_file_formats,
        compressed_file_formats=compressed_file_formats,
    )
    extraction_fields = config["EXTRACTION_FIELDS"]
    csv_file_path = config["CSV_FILE_PATH"]
    system_role_content = config["SYSTEM_ROLE_CONTENT"]

    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    info_extraction_pipeline(
        textual_folder=textual_folder,
        extraction_fields=extraction_fields,
        csv_file_path=csv_file_path,
        api_key=api_key,
        system_role_content=system_role_content,
    )


if __name__ == "__main__":
    main()
