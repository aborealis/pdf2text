# PDF-to-Text Converter

This is a command-line tool that converts multi-page PDF files to a text using the `pytesseract` Python package. The script first converts each page of PDF into image, and then optically recognizes the text from each image file, using OCR technology. The resulted text is written into `result.txt` file in the script's directory.

## Requirements

To use `pytesseract` package (for converting images to text), please install OCR in your system:

* For OCR core installation on Ubuntu/Debian, please run: `sudo apt-get install tesseract-ocr`
* [Optional] To install additional language-specific library to convert PDF files with non-English glyphs, run: `sudo apt-get install tesseract-ocr-[lang]`. For instance, to convert Russian pdf-files, run `sudo apt-get install tesseract-ocr-rus` to recognize cyrillic glyphs.

## Script Installation

I suggest to use `pipenv` command to install necessary packages into a separate virtual environment. It allows to easily remove the script and all dependencies once you stop using it, and keep your system clean. If you don't have `pipenv` installed, simply run `python -m pip install pipenv`. Now follow these steps:

1. Clone this repo `git clone https://github.com/aborealis/pdf2text`
2. Change dir `cd pdf2text`.
3. Run `pipenv install` to install dependencies within a virtual environment.
4. Run `pipenv shell` to enter virtual environment

Now you can use the script as described in the next section.

To exit virtual environment, please type `exit`

To remove your virtual environment and uninstall the script, simply

1. Change dir `cd pdf2text`.
2. Run `pipenv --rm` to remove virtual environment. Be sure to exit virtual environment first.
3. Delete `pdf2text` folder.

## Usage

```
usage: A multi-page PDF-to-text convertor. [-h] -i INPUT [-l LANGUAGE] [-w WORKERS]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        a full path to the PDF-file
  -l LANGUAGE, --language LANGUAGE
                        language of the text, e.g., rus, lat, etc. (default: eng). Use it
                        to convert a PDF from a language with a specific characters. Please
                        install the OCR language library first. For example, run 'sudo
                        apt-get install tesseract-ocr-rus' to install the Russian OCR
                        recognition library.
  -w WORKERS, --workers WORKERS
                        sets number of pages the script will convert at a time. Use it to
                        accelirate the execution. The number of concurrent pages should not
                        exceed the number of you cores/CPUs minus one. Leave at least one
                        core/CPU to handle your OS, while other are busy with conversion.

```

## Examples

Convert a PDF file with English characters to a text:

```
$ python pdf2text.py -i path/to/file.pdf
```

Convert a PDF file with Russian characters to a text (P.S. Don't forget to install a language-specific library, see 'requirements' section):

```
$ python pdf2text.py -i path/to/file.pdf -l rus
```

Convert a PDF with 2 pages at a time (assuming I have at least 3 cores/CPUs)

```
$ python pdf2text.py -i path/to/file.pdf -w 2
```

## License

This project is licensed under the MIT License.