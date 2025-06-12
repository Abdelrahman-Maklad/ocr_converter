# OCR Document Converter
# Copyright (c) 2025 - Licensed under MIT License

import os
import cv2
import pytesseract
from PyPDF2 import PdfWriter, PdfReader
from pdf2image import convert_from_path
import concurrent.futures
import time
from random import random
from pathlib import Path
from tqdm import tqdm
from rich.console import Console
from rich.markdown import Markdown


def convert_to_images(input_path: str, output_folder: str) -> list:
    """
    Convert PDF pages to images
    
    Args:
        input_path: Path to input PDF file
        output_folder: Folder to save converted images
        
    Returns:
        list: Paths to converted image files
    """
    FORMAT = 'jpg'
    FIRST_PAGE = None
    LAST_PAGE = None
    USE_CROPBOX = False
    STRICT = False
    POPPLER_PATH = r'poppler-23.05.0\Library\bin'

    pil_images = convert_from_path(input_path, output_folder=output_folder, first_page=FIRST_PAGE,
                                   last_page=LAST_PAGE, fmt=FORMAT, userpw=None, use_cropbox=USE_CROPBOX,
                                   strict=STRICT, poppler_path=POPPLER_PATH)

    return pil_images


def perform_ocr_and_save_to_pdf(image_file, pdf_writer):
    """
    Perform OCR on image file and save the result to PDF writer
    
    Args:
        image_file: Path to the image file
        pdf_writer: PdfWriter object to write the OCR result to PDF
    """
    tool_path = str(Path.cwd())
    pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
    TESSDATA_PREFIX = r'Tesseract-OCR'
    tessdata_dir_config = fr'--tessdata-dir "{tool_path}\Tesseract-OCR\tessdata"'
    img = cv2.imread(image_file, 1)
    result = pytesseract.image_to_pdf_or_hocr(img, lang="eng",
                                              config=tessdata_dir_config)  # Use pytesseract default config

    temp_pdf_path = os.path.splitext(image_file)[0] + '_temp.pdf'
    with open(temp_pdf_path, 'wb') as temp_pdf_file:
        temp_pdf_file.write(result)

    with open(temp_pdf_path, 'rb') as temp_pdf_file:
        pdf_page = PdfReader(temp_pdf_file).pages[0]
        pdf_writer.add_page(pdf_page)

    os.remove(temp_pdf_path)


def process_pdf(link):
    """
    Process the PDF file: convert to images, perform OCR, and save as new PDF
    
    Args:
        link: Path to the input PDF file
        
    Returns:
        str: Result message
    """
    try:
        tool_path = str(Path.cwd())
        link = link.strip()
        output_dir = "OCR_file"
        pdf_filename = os.path.splitext(os.path.basename(link))[0] + str(random()).replace(".", "")
        pdf_path = os.path.join(output_dir, f'{pdf_filename}.pdf')
        image_folder = os.path.join(output_dir, f'{pdf_filename}_images')
        os.makedirs(image_folder, exist_ok=True)

        convert_to_images(link, image_folder)

        pdf_writer = PdfWriter()

        for filename in os.listdir(image_folder):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                image_file = os.path.join(image_folder, filename)
                perform_ocr_and_save_to_pdf(image_file, pdf_writer)

        with open(pdf_path, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

        return f"{link}\t{tool_path}\\{pdf_path}"
    except Exception as E:
        return f"{link}\t{E}"


if __name__ == '__main__':
    console = Console()

    title = '''# OCR CONVERTER
    > this tool is designed for the following purposes:
        1- convert the unsearchable document into searchable and create a new document with a given path.

    '''
    title = Markdown(title)
    console.print(title)

    with open("ocr_input.txt", 'r') as f:
        links_list = f.readlines()

    one_time_count = 5

    with tqdm(total=len(links_list), desc=f"Processing".upper(), unit="document", ncols=100) as progress_bar:
        with concurrent.futures.ProcessPoolExecutor(max_workers= 2) as executor:
            for i in range(0, len(links_list), one_time_count):
                batch_links = links_list[i:i + one_time_count]
                results = executor.map(process_pdf, batch_links)
                for result in results:
                    with open('ocr_output.txt', 'a', encoding='utf8') as of:
                        of.write(result)
                        of.write('\n')
                        progress_bar.update(1)

        progress_bar.set_description(f"done".upper())

