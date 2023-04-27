"""
Requirements:

To use `pytesseract` (for converting images to text), please
install `tesseract-ocr` in your system:

* To install OCR on Debian Linux, run: `sudo apt-get install
tesseract-ocr`
* [Optional] To install language-specific library, run: `sudo
apt-get install tesseract-ocr-<lang>`. For instance, to
recognize Russian pdf-files, run `sudo apt-get install
tesseract-ocr-rus`.
"""

import argparse
import pytesseract
from pdf2image import convert_from_path
from tqdm import tqdm
import PyPDF2

# Script arguments parsers
parser = argparse.ArgumentParser(
    description='A multi-page PDF-to-text convertor.')
parser.add_argument(
    '-i', '--input',
    type=str,
    help='a full path to the PDF-file'
)
parser.add_argument(
    '-l', '--language',
    nargs='?',
    const='eng',
    default=None,
    help='Language of the text, e.g., rus, lat, etc. (default: eng). To convert a PDF from a specific language, please install the OCR language library. For example, run `sudo apt-get install tesseract-ocr-rus` to install the Russian OCR recognition library.'
)

# Get script's arguments
args = parser.parse_args()

# Check if file path exists
if not args.input:
    print("No file path found. See --help for details")
    exit()

# Get PDF file path and PDF file language
pdf_path = args.input
pdf_lang = args.language

# Get number of pages in PDF file
with open(pdf_path, 'rb') as f:
    pdf_reader = PyPDF2.PdfReader(f)
    num_pages = len(pdf_reader.pages)


output_text = ''
# Convert each page into a PNG-image and then image to a regular text
for page in tqdm(range(num_pages), desc="Converting"):
    page_pdf = convert_from_path(pdf_path, first_page=page, last_page=page)
    if not page_pdf:
        continue
    page_png = page_pdf[0].convert('RGB')
    text = pytesseract.image_to_string(page_png, lang=pdf_lang)
    output_text += f'{text}\n'

# Write results into the current directory
with open('result.txt', 'w', encoding='utf-8') as file:
    file.write(output_text)
