"""
A simple PDF-to-Text Converter.
https://github.com/aborealis/pdf2text
"""

import time
import os
from argparse import Namespace, ArgumentParser
import pytesseract
from pdf2image import convert_from_path
from tqdm import tqdm
import PyPDF2
from concurrent import futures


def get_arguments() -> Namespace:
    """
    Parses the script's arguments and check if they are valid.
    Also sets the description and output of --help argument
    """
    description = 'A multi-page PDF-to-text convertor.'
    args = [
        dict(
            arg='input',
            default=None,
            required=True,
            type=str,
            help='a full path to the PDF-file'
        ),
        dict(
            arg='language',
            default=None,
            required=False,
            type=str,
            help='language of the text, e.g., rus, lat, etc. (default: eng). Use it to convert a PDF from a language with a specific characters. Please install the OCR language library first. For example, run `sudo apt-get install tesseract-ocr-rus` to install the Russian OCR recognition library.'
        ),
        dict(
            arg='workers',
            default=1,
            required=False,
            type=int,
            help='sets number of pages the script will convert at a time. Use it to accelirate the execution. The number of concurrent pages should not exceed the number of you cores/CPUs minus one. Leave at least one core/CPU to handle your OS, while other are busy with conversion.'
        ),
    ]

    parser = ArgumentParser(description)
    for arg in args:
        parser.add_argument(
            f"-{arg['arg'][0]}",
            f"--{arg['arg']}",
            type=arg['type'],
            default=arg['default'],
            required=arg['required'],
            help=arg['help'],
        )

    # Get script's arguments
    args = parser.parse_args()

    # Check if file path exists and correct
    file_path = args.input
    if not file_path:
        print('No file path found. See --help for details')
        exit()
    if not os.path.isfile(file_path):
        print('No pdf file found in the location you specified')
        exit()
    if os.path.splitext(file_path)[1] != '.pdf':
        print('The file specified is not a PDF file. Please indicate the path to a file with *.pdf extension')
        exit()
    if args.workers <= 0:
        args.workers = 1

    return args


def convert_page(args: Namespace,
                 page: int) -> str:
    """
    Convert a single page into an image,
    and then image to a regular text
    """
    path = args.input
    lang = args.language
    page_pdf = convert_from_path(
        path,
        first_page=page,
        last_page=page,
    )
    if not page_pdf:
        return ''
    page_img = page_pdf[0].convert('RGB')
    text = pytesseract.image_to_string(page_img, lang=lang)
    return text


def get_num_pages(args: Namespace) -> int:
    """
    Returns total number of pages in PDF
    file with help of PyPDF2 package
    """
    path = args.input
    with open(path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        num_pages = len(pdf_reader.pages)
    return num_pages


def scan() -> str:
    """
    This function scans a PDF document by creating a pool
    of future processes, each of which processes one page
    of the document at a time. It then distributes these
    processes to N simultaneous workers to speed up the execution.
    """
    args = get_arguments()
    with futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        num_pages = get_num_pages(args)

        # Create a queue of future tasks
        queue = []
        for page in range(num_pages):
            # Submit a task to the pool
            task = executor.submit(
                convert_page,
                args,
                page,
            )
            # Append the task to the queue
            queue.append(task)

        output_text = ''
        # Iterate over the completed futures and process the results
        for task in tqdm(futures.as_completed(queue), total=num_pages, desc=f"Converting {args.workers} pages at a time"):
            text = task.result()
            output_text += f'{text}\n'
            time.sleep(0.1)

        return output_text


# Write results into the current directory
scanned_text = scan()
with open('result.txt', 'w', encoding='utf-8') as file:
    file.write(scanned_text)
