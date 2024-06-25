import os
import re
from pdfminer.high_level import extract_text
from datetime import datetime
import mysql.connector
from Ledger.Post_transaction import Add_Transaction
from Refresh_db import update_all_accounts

post_transaction = Add_Transaction()
update = update_all_accounts.update_all_accounts()

class line_extract:
    @classmethod
    def extract_lines(cls,db_host, db_user, db_password, db_name,file_path):
        user_home = os.path.expanduser("~")
        
        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = db_connection.cursor()

        # Extract text from the entire PDF
        pdf_text = extract_text(file_path)

        # Split the text into lines
        lines = pdf_text.split('\n')
        return_list = []
        
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
        
        def find_recurring_transactions(note, table_name):
            query = f"""SELECT Category FROM {table_name}
                    WHERE Note LIKE '%{note.replace("'", "''")}%'
                    ORDER BY CHAR_LENGTH(Note) - CHAR_LENGTH(REPLACE(Note, ' ', '')) DESC, CHAR_LENGTH(Note) DESC
                    LIMIT 1;"""
            cursor.execute(query)
            row = cursor.fetchone()

            if row is not None:
                return row[0]
            else:
                return None
        date_line = 4
        
        
        test = use_multi_regex(lines[date_line],[r'\b(\w+ \d{1,2}, \d{4}) through (\w+ \d{1,2}, \d{4})\b'])
        if test != True:
            date_line = 25
            
        
        
            
        starting_date_index = lines[date_line]
        starting_date = starting_date_index.split()
        
        
            
        
        inserted = 1  # Initialize the inserted count outside the loop
        i = 111  # Start from line 111

        while i < len(lines):
            line = lines[i]

            # Inside the loop where you process transaction details
            if use_multi_regex(line, regex_list):
            
                # Extract the date and year
                date_match = re.search(r"^\d\d/\d\d", line)
                if date_match:
                    # Get the date in mm/dd format
                    transaction_date = date_match.group()

                    # Extract the year from the line (assuming it's in a specific position)
                    year = starting_date[-1]
                    start_year = year  # Store the year as-is

                    # Extract the day from the line and remove commas
                    day = starting_date[1]
                    start_day = day.replace(',', '')

                    # Concatenate the year with the date
                    transaction_date += f'/{year}'
                    format_date = transaction_date
                    transaction_date = datetime.strptime(format_date, '%m/%d/%Y').strftime('%Y-%m-%d')


                # Start processing the next 6 lines
                for x in range(1, 7):
                    i += 1  # Move to the next line
                    line = lines[i]
                    if x == 2:
                        # Get the note
                        transaction_note = line.replace("  ", "")
                    elif x == 4:
                        # Extract the amount from the line (allowing for amounts greater than 1,000)
                        amount_match = re.search(r"[+-]?\d{1,3}(,\d{3})*\.\d{2}", line)
                        if amount_match:
                            # Remove commas and convert to float
                            amount_str = amount_match.group().replace(",", "")
                            transaction_amount = float(amount_str)
                            if transaction_amount < 0:
                                transaction_Type = "Expense-Unsorted"
                                transaction_amount = abs(transaction_amount)
                            else:
                                transaction_Type = "Income-Unsorted"
                                transaction_amount = abs(transaction_amount)
                        bank_verified = True
                        account = "Checking_Account"
                        
                        date = transaction_date
                        transaction_date = datetime.strptime(transaction_date,"%Y-%m-%d")
                        # Access the year attribute after ensuring start_date is a datetime object
                        year = transaction_date.year
                        table_name = f"Budget{year}"
                        posted_table_name = f"Posted_transactions_{year}"
                        transaction_ID = None
                        
                        if transaction_Type == "Income-Unsorted":
                            # Fetch the row
                            query = f"SELECT * FROM {table_name} WHERE date = %s"
                            cursor.execute(query, (date,))
                            row = cursor.fetchone()

                            if row is not None:
                                # Check if 'Income' column (at index 8) is 'null' and handle accordingly
                                income_index = 8
                                current_income = 0.00 if row[income_index] == 'null' else float(row[income_index])

                                final_income = current_income + transaction_amount

                                insert_query = f"""
                                    INSERT INTO {table_name} (date,Income)
                                    VALUES (%s,%s)
                                    ON DUPLICATE KEY UPDATE
                                    Income = VALUES(Income) 
                                """
                                insert_values = (
                                    date,  
                                    final_income
                                    )
                                
                                new_sub_category = find_recurring_transactions(transaction_note, posted_table_name)
                                if new_sub_category != None:
                                    transaction_Type = new_sub_category
    
                                try:
                                    cursor.execute(insert_query, insert_values)
                                    db_connection.commit()
                                    # Get the ID of the last inserted row
                                    last_inserted_id = cursor.lastrowid
                                    # Get the number of affected rows
                                    num_affected_rows = cursor.rowcount
                                    #print(f"Data inserted successfully. Last Inserted ID: {last_inserted_id}, Affected Rows: {num_affected_rows}")
                                    transaction_ID = post_transaction.Add_Transaction(db_host, db_user, db_password, db_name, date, "Checking_Account", transaction_note, transaction_amount, "Income",transaction_Type,bank_verified)
                                    
                                except mysql.connector.Error as err:
                                    print(f"Error: {err}")
                                
                            else:
                                print(f"No expense found for {date}")
                        
                        elif transaction_Type == "Expense-Unsorted":
                            # Fetch the row
                            query = f"SELECT * FROM {table_name} WHERE date = %s"
                            cursor.execute(query, (date,))
                            row = cursor.fetchone()

                            if row is not None:
                                # Check if 'Expenses' column (at index 9) is 'null' and handle accordingly
                                expense_index = 9
                                current_expense = 0.00 if row[expense_index] == 'null' else float(row[expense_index])

                                final_expense = current_expense + transaction_amount

                                insert_query = f"""
                                    INSERT INTO {table_name} (date,Expenses)
                                    VALUES (%s,%s)
                                    ON DUPLICATE KEY UPDATE
                                    Expenses = VALUES(Expenses) 
                                """
                                insert_values = (
                                    date,  
                                    final_expense
                                    )
                                new_sub_category = find_recurring_transactions(transaction_note, posted_table_name)
                                if new_sub_category != None:
                                    transaction_Type = new_sub_category
                                
                                try:
                                    cursor.execute(insert_query, insert_values)
                                    db_connection.commit()
                                    # Get the ID of the last inserted row
                                    last_inserted_id = cursor.lastrowid
                                    # Get the number of affected rows
                                    num_affected_rows = cursor.rowcount
                                    #print(f"Data inserted successfully. Last Inserted ID: {last_inserted_id}, Affected Rows: {num_affected_rows}")
                                    transaction_ID = post_transaction.Add_Transaction(db_host, db_user, db_password, db_name, date, "Checking_Account", transaction_note, transaction_amount, "Expense", transaction_Type,bank_verified)
                                    
                                except mysql.connector.Error as err:
                                    print(f"Error: {err}")
                                
                            else:
                                print(f"No expense found for {date}")
                        
                        
                        list_format = [
                            transaction_ID,
                            date,
                            account,
                            transaction_note,
                            transaction_amount,
                            transaction_Type,
                            bank_verified
                        ]
                        return_list.append(list_format)
            i += 1
            
        
        update.Update_all_accounts(db_host, db_user,db_password,db_name,table_name,year)
        db_connection.commit()
        cursor.close()
        return return_list
            


#source myenv/bin/activate
