from config import load_config
import os
from src.convert_between_formats.convert_to_text_pipeline import pipeline

def main():
    # Load configuration
    config = load_config('config.json')

    # Access path values throught configuration values
    input_folder = config.get('input_folder')
    extracted_zips_folder = config.get('extracted_zips_folder')
    final_folder = config.get('final_folder')
    processed_images_folder = config.get('processed_images_folder')

    os.makedirs(extracted_zips_folder, exist_ok=True)
    os.makedirs(final_folder, exist_ok=True)
    os.makedirs(processed_images_folder, exist_ok=True)

    pipeline(input_folder = input_folder,
             extracted_zips_folder=extracted_zips_folder,
             final_folder=final_folder,
             processed_images_folder=processed_images_folder)


if __name__ == "__main__":
    main()