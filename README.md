# OCR Converter Tool

A tool for converting scanned documents and images to searchable text using Tesseract OCR.

## Features

- Supports multiple input formats:
  - PDF files
  - Image files (PNG, JPG, TIFF)
- Batch processing capability
- Multi-language support
- Preserves document structure
- Outputs searchable PDF files

## Requirements

- Python 3.7+
- Required packages:
  - tesseract-ocr
  - poppler
  - pdf2image
  - pytesseract
  - Pillow

## Installation

1. Install dependencies:
```bash
pip install pytesseract pdf2image Pillow
```

2. Install Tesseract OCR:
- Included in tesseract-ocr folder
- Or download from https://github.com/UB-Mannheim/tesseract/wiki

3. Install Poppler:
- Included in poppler-23.05.0 folder
- Or download from https://github.com/oschwartz10612/poppler-windows/releases

## Usage

1. Create an input file (ocr_input.txt) with list of files to process

2. Run the tool:
```bash
python Ocr_converter.py
```

3. Converted files will be saved in OCR_file directory

## Output

- Searchable PDF files
- Text extraction results
- Processing log

## License

MIT License - See LICENSE file for details
