import os
from pdfminer.high_level import extract_text

user_home = os.path.expanduser("~")

def upload_file(file_path):

    # Extract text from the entire PDF
    pdf_text = extract_text(file_path)

    # Split the text into lines
    lines = pdf_text.split('\n')

    # Print each line with an index number
    for i, line in enumerate(lines):
        print(f"{i}: {line}")

upload_file('/Users/kerinpatel/Desktop/20240123-statements-1859--2.pdf')

