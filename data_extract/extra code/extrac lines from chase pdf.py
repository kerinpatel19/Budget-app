import os
from pdfminer.high_level import extract_text

user_home = os.path.expanduser("~")

def upload_file(file_path):

    # Extract text from the entire PDF
    pdf_text = extract_text(file_path)

    # Split the text into lines
    lines = pdf_text.split('\n')

    # Initialize a list to hold the formatted data
    transactions = []

    # Variables to hold transaction details
    eff_date, syst_date, description, amount = None, None, None, None

    # Iterate through each line to extract and classify transactions
    for i, line in enumerate(lines):
        if "Eff. Date" in line:
            eff_date = lines[i + 1].strip()
        elif "Syst. Date" in line:
            syst_date = lines[i + 1].strip()
        elif "Description" in line:
            description = lines[i + 1].strip()
        elif line.startswith("$"):  # Assuming amount lines start with '$'
            amount = line.strip()
            # Determine if the transaction is an income or an expense based on the description or other criteria
            transaction_type = "income" if "Deposit" in description or "Credit" in description else "expense"
            # Append the transaction to the list
            transactions.append((eff_date, syst_date, description, amount, transaction_type))
            # Reset variables for the next transaction
            eff_date, syst_date, description, amount = None, None, None, None

    # Example: Print the formatted data
    for transaction in transactions:
        print(f"Eff Date: {transaction[0]}, Syst Date: {transaction[1]}, Description: {transaction[2]}, Amount: {transaction[3]}, Type: {transaction[4]}")

upload_file('/Users/kerinpatel/Desktop/Discoverbank-Statement-20240430-3553.pdf')
#/Users/kerinpatel/Desktop/data/20240314-statements-0651-.pdf
#/Users/kerinpatel/Desktop/data/20240214-statements-0651-.pdf
