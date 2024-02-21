import os
import re
from pdfminer.high_level import extract_text
from datetime import datetime

class line_extract:
    @classmethod
    def extract_lines(file_path):
        user_home = os.path.expanduser("~")

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
        date_idex_line = 4
        starting_date_index = lines[date_idex_line]
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
                        transaction_note = line
                    elif x == 4:
                        # Extract the amount from the line (allowing for amounts greater than 1,000)
                        amount_match = re.search(r"[+-]?\d{1,3}(,\d{3})*\.\d{2}", line)
                        if amount_match:
                            # Remove commas and convert to float
                            amount_str = amount_match.group().replace(",", "")
                            transaction_amount = float(amount_str)
                    
                        list_format = [
                            transaction_date,
                            transaction_note,
                            transaction_amount,
                        ]
                        return_list.append(list_format)
            i += 1
        return return_list
            


#source venv/bin/activate