import os
import sys
sys.path.insert(0,"src/convert_between_formats/")
from image_preprocessing import preprocess_image

import zipfile
import pandas as pd
from docx import Document
from pdf2image import convert_from_path
import cv2 as cv

class FileProcessor:
    def __init__(self, extracted_zips_folder, final_folder, processed_images_folder):
        self.extracted_zips_folder = extracted_zips_folder
        self.final_folder = final_folder
        self.processed_images_folder = processed_images_folder

    def process_file(self, input_path):
        """
        Process a file based on its extension.
        """
        filename, file_extension = os.path.splitext(input_path)
        file_extension = file_extension.lower()
        base_filename = os.path.basename(filename)

        if file_extension == '.docx':
            text = self.extract_text_from_docx(input_path)
            self.save_text_to_file(text, base_filename)
        elif file_extension == '.doc':
            self.process_doc_file(input_path, base_filename)
        elif file_extension == '.xlsx':
            text = self.extract_text_from_xlsx(input_path)
            self.save_text_to_file(text, base_filename)
        elif file_extension == '.zip':
            self.extract_zip(input_path, self.extracted_zips_folder)
        elif file_extension in ['.jpg', '.jpeg', '.png', '.tif', '.tiff']:
            output_path = os.path.join(self.processed_images_folder, f"{base_filename}.png")
            self.process_image(input_path, output_path)
        elif file_extension == '.pdf':
            self.process_pdf(input_path, self.processed_images_folder)
        else:
            print(f"Unsupported file format: {file_extension}")


    def extract_text_from_docx(self, docx_path):
        """
        Extract text from a DOCX file.
        """
        doc = Document(docx_path)
        full_text = [para.text for para in doc.paragraphs]
        return '\n'.join(full_text)

    def extract_text_from_xlsx(self, xlsx_path):
        """
        Extract text from an XLSX file.
        """
        df = pd.read_excel(xlsx_path)
        return df.to_string()

    def extract_zip(self, zip_path, extract_to):
        """
        Extract a ZIP file to a specified directory.
        """
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

    def process_image(self, image_path, output_path):
        """
        Process an image and save it to the output path.
        """
        image = cv.imread(image_path)
        processed_image = preprocess_image(image)
        cv.imwrite(output_path, processed_image)

    def process_pdf(self, pdf_path, output_path):
        """
        Process a PDF file and save each page as an image.
        """
        images = convert_from_path(pdf_path)
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        pdf_folder = os.path.join(output_path, pdf_name)
        os.makedirs(pdf_folder, exist_ok=True)
        for i, image in enumerate(images):
            image_output_path = os.path.join(pdf_folder, f"{pdf_name}_page_{i+1}.png")
            image.save(image_output_path, "PNG")
            self.process_image(image_output_path, image_output_path)
    def save_text_to_file(self, text, base_filename):
        """
        Save text to a file in the final folder.
        """
        output_path = os.path.join(self.final_folder, f"{base_filename}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)

    def process_doc_file(self, input_path, base_filename):
        """
        Process DOC file using the 'antiword' command.
        """
        output_path = os.path.join(self.final_folder, f"{base_filename}.txt")
        os.system(f'antiword "{input_path}" > "{output_path}"')

