import os
import sys
sys.path.insert(0,"src/convert_between_formats/")
from file_processor import FileProcessor


def get_all_files(input_folder):
    file_paths = []
    for root, dirs, files in os.walk(input_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_paths.append(file_path)
    return file_paths


def pipeline(
    input_folder,
    extracted_zips_folder,
    final_folder,
    processed_images_folder
):
    input_files = get_all_files(input_folder=input_folder)
    file_processor = FileProcessor(
        extracted_zips_folder=extracted_zips_folder,
        final_folder=final_folder,
        processed_images_folder=processed_images_folder)

    for input_file in input_files:
        print(f'--- {input_file} ---')
        file_processor.process_file(input_path=input_file)

    print("-"*40,'\n moving to extracted zips')
    extracted_files = get_all_files(input_folder=extracted_zips_folder)
    for input_file in extracted_files:
        print(f'--- {input_file} ---')
        file_processor.process_file(input_path=input_file)

if __name__ == '__main__':

    # Define paths
    base_data_path = './data_clone/'
    raw_data_path = base_data_path + 'raw/'
    files_source_path = raw_data_path + 'scrapped_documents/'
    extracted_zips_folder = raw_data_path + 'extracted_zips/'
    input_folder = files_source_path
    processed_data_path = base_data_path + 'processed/'
    final_folder = processed_data_path+'final'
    processed_images_folder = processed_data_path + 'processed_images'

    pipeline(input_folder = input_folder,
             extracted_zips_folder=extracted_zips_folder,
             final_folder=final_folder,
             processed_images_folder=processed_images_folder)
    #pipeline()
