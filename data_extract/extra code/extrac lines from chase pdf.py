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
        if i == 50:
            break

upload_file('/Users/kerinpatel/Desktop/data/20240314-statements-0651-.pdf')
#/Users/kerinpatel/Desktop/data/20240314-statements-0651-.pdf
#/Users/kerinpatel/Desktop/data/20240214-statements-0651-.pdf
