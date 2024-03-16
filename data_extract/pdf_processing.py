import os
from pdfminer.high_level import extract_text
import re
import mysql.connector
from datetime import datetime

# Database connection parameters
db_host = 'localhost'
db_user = 'root'
db_password = 'Panna4120@'
db_name = 'Database2023'

# Establish a connection to MySQL
db_connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

cursor = db_connection.cursor()


user_home = os.path.expanduser("~")
Expenses = {'Petsmart': {'new_note': 'Dog and cat food', 'categories': 'NOTES_PETS'},
            'Jimmy Johns': {'new_note': 'Jimmy Johns', 'categories': 'NOTES_FOOD'},
            'Amc Online': {'new_note': 'Amc movies', 'categories': 'NOTES_FOOD'},
            'Hy-Vee': {'new_note': 'Hy-Vee', 'categories': 'NOTES_FOOD'},
            'Panda Express': {'new_note': 'Panda Express', 'categories': 'NOTES_FOOD'},
            'Target': {'new_note': 'Target shopping', 'categories': 'NOTES_WANTS'},
            'Apple Cash': {'new_note': 'Apple Cash', 'categories': 'NOTES_OTHER'},
            'Urgent Care': {'new_note': 'Urgent Care', 'categories': 'NOTES_OTHER'},
            'Amazon Prime': {'new_note': 'Amazon Prime', 'categories': 'NOTES_FIXED_EXPENSE'},
            'Netflix.Com': {'new_note': 'Apple Cash', 'categories': 'NOTES_FIXED_EXPENSE'},
            'Discover Bank': {'new_note': 'Discover loan', 'categories': 'NOTES_LONG_TERM_LOANS'},
            'Sofi Bank': {'new_note': 'Bella loan sofi', 'categories': 'NOTES_LONG_TERM_LOANS'},
            'Allstate Ins': {'new_note': 'Tesla car insurance', 'categories': 'NOTES_FIXED_EXPENSE'},
            'Sonic Drive IN': {'new_note': 'Sonic Drive IN', 'categories': 'NOTES_FOOD'},
            'Monthly Service Fee': {'new_note': 'Monthly Service Fee', 'categories': 'NOTES_FIXED_EXPENSE'},
            'Online Transfer From Chk ...1859': {'new_note': 'income from kerins account', 'categories': 'NOTES_INCOME'},
            'Online Transfer From Chk ...4239': {'new_note': 'income from Bellas account', 'categories': 'NOTES_INCOME'},
            }

categories = {1: 'NOTES_LONG_TERM_LOANS',
              2: 'NOTES_SHORT_TERM_CREDIT',
              3: 'NOTES_FIXED_EXPENSE',
              4: 'NOTES_WANTS',
              5: 'NOTES_PETS',
              6: 'NOTES_MAJOR_PURCHASES',
              7: 'NOTES_FOOD',
              8: 'NOTES_GOING_OUT2',
              9: 'NOTES_OTHER',
              10: 'NOTES_INCOME'
              }

month_name_to_number = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

last_date = []
def process_pdf_file(file_name):
    user_home = os.path.expanduser("~")  # Define user_home inside the function

    transactions = []
    # Define the PDF file path
    pdf_directory = os.path.join(user_home, "Desktop", "Budget app", "Files to upload")
    pdf_file_path = os.path.join(pdf_directory, file_name)

    # Extract text from the entire PDF
    pdf_text = extract_text(pdf_file_path)

    # Split the text into lines
    lines = pdf_text.split('\n')

    # Define a function to use a regex pattern for filtering lines
    def use_multi_regex(input_text, regex_list):
        for regex_pattern in regex_list:
            if re.search(regex_pattern, input_text, re.IGNORECASE):
                return True
        return False

    # List of regex patterns to check for different transaction details
    regex_list = [
        r"^\d\d/\d\d",  # Date format (mm/dd)
    ]
    date_idex_line = 4
    starting_date_index = lines[date_idex_line]
    starting_date = starting_date_index.split()
    print(starting_date)
    # Input components
    month_name = starting_date[0]
    day = starting_date[1]
    year = starting_date[2]

    # Assuming month_name_to_number is your mapping of month names to numbers
    month_number = month_name_to_number.get(month_name)

    # Remove the comma from day and convert to an integer
    day = int(day.replace(',', ''))

    # Convert year to an integer
    year = int(year)

    # Create a datetime object and format it as 'YYYY-MM-DD'
    starting_formatted_date = f'{year}-{month_number:02d}-{day:02d}'


    month_name = starting_date[0]
    beginning_balance = lines[69]
    starting_bal = beginning_balance[1:]
    starting_balance = float(starting_bal)
    #print(beginning_balance)

    last_date = []
    current_expense = []
    income = []
    current_balance = []
    notes = []
    bank_balance = 0.0
    current_balance.append(starting_balance)

    last_date.append(starting_formatted_date)  # Initialize last_date


    inserted = 1  # Initialize the inserted count outside the loop
    i = 111  # Start from line 111

    while i < len(lines):
        line = lines[i]

        # Inside the loop where you process transaction details
        if use_multi_regex(line, regex_list):
            # Initialize transaction details
            transaction = {'date': 'null', 'note': 'null', 'amount': 0.0, 'current_balance': 0.0, 'categories': 'NOTES_OTHER'}

            # Extract the date and year
            date_match = re.search(r"^\d\d/\d\d", line)
            if date_match:
                # Get the date in mm/dd format
                transaction['date'] = date_match.group()

                # Extract the year from the line (assuming it's in a specific position)
                year = starting_date[-1]
                start_year = year  # Store the year as-is

                # Extract the day from the line and remove commas
                day = starting_date[1]
                start_day = day.replace(',', '')

                # Convert the month name to month number
                if month_name in month_name_to_number:
                    start_month_number = month_name_to_number[month_name]

                # Concatenate the year with the date
                transaction['date'] += f'/{year}'
                format_date = transaction['date']
                transaction['date'] = datetime.strptime(format_date, '%m/%d/%Y').strftime('%Y-%m-%d')


            # Start processing the next 6 lines
            for x in range(1, 7):
                i += 1  # Move to the next line
                line = lines[i]
                if x == 2:
                    # Get the note
                    transaction['note'] = line
                elif x == 4:
                    # Extract the amount from the line (allowing for amounts greater than 1,000)
                    amount_match = re.search(r"[+-]?\d{1,3}(,\d{3})*\.\d{2}", line)
                    if amount_match:
                        # Remove commas and convert to float
                        amount_str = amount_match.group().replace(",", "")
                        transaction['amount'] = float(amount_str)
                elif x == 6:
                    # Extract the current balance from the line (allowing for amounts greater than 1,000)
                    balance_match = re.search(r"[+-]?\d{1,3}(,\d{3})*\.\d{2}", line)
                    if balance_match:
                        # Remove commas and convert to float
                        balance_str = balance_match.group().replace(",", "")
                        transaction['current_balance'] = float(balance_str)

            # Continue processing the transaction as before

            # Match the transaction note to an expense name and set the appropriate category
            for expense in Expenses.keys():
                if expense in transaction['note']:
                    transaction['categories'] = Expenses[expense]['categories']
                    transaction['note'] = Expenses[expense]['new_note']
                    #print('Inserted successfully')
                    # print(inserted, "   ", transaction['date'], transaction['note'], transaction['amount'], transaction['categories'])
                    inserted += 1
                    transactions.append(transaction)

                    # Insert data into the appropriate month table
                    insert_data_query = f"INSERT INTO pending_transactions (TRANSACTION_DATE, NOTE, AMOUNT, CATEGORYS) VALUES (%s, %s, %s, %s)"
                    data = (
                    transaction['date'], transaction['note'], transaction['amount'],
                    transaction['categories'])
                    cursor.execute(insert_data_query, data)
                    break

            if 'categories' not in transaction:
                transaction['categories'] = 'NOTES_UNKNOWN'

                #print('Inserted successfully - default ')
                #print(inserted, "   ", transaction['date'], transaction['note'], transaction['amount'],
                      #transaction['categories'])
                transactions.append(transaction)

            







        i += 1


    return transactions  # Return the list of transactions

if __name__ == "__main__":
    pdf_file_name = 'chase_statement.pdf'  # Replace with the actual PDF file name
    process_pdf_file(pdf_file_name)

db_connection.commit()
cursor.close()
db_connection.close()
