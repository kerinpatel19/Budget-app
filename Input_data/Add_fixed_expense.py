import mysql.connector
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from Ledger.Post_transaction import Add_Transaction
from Refresh_db.update_checking import update_checking_account


post_transaction = Add_Transaction()
checking_account_update = update_checking_account()

class Add_fixed_expense:
    @classmethod
    
    def Add_Fixed_expense(cls, db_host, db_user, db_password, db_name, start_date, note, amount, sub_category,Bank_verified):
        # Convert start_date to a datetime object if it's a string
        if isinstance(start_date, str):
            start_date_1 = datetime.strptime(start_date, '%Y-%m-%d')

        # Access the year attribute after ensuring start_date is a datetime object
        year = start_date_1.year
        table_name = f"Budget{year}"
        

        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = db_connection.cursor()
        
        current_date = start_date
        end_date = f"{year}-12-31"
        # Convert the string to a datetime object
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        # Convert the string to a datetime object
        current_date = datetime.strptime(current_date, '%Y-%m-%d')

        while current_date.strftime('%Y-%m-%d') < end_date.strftime('%Y-%m-%d'):
            # print(f"current date :{current_date} End_date :{end_date}")
            print (current_date)

            # Fetch the row
            query = f"SELECT * FROM {table_name} WHERE date = %s"
            cursor.execute(query, (current_date,))
            row = cursor.fetchone()

            if row is not None:
                # Check if 'Expenses' column (at index 9) is 'null' and handle accordingly
                expense_index = 9
                current_expense = 0.00 if row[expense_index] == 'null' else float(row[expense_index])

                final_expense = current_expense + amount

                insert_query = f"""
                    INSERT INTO {table_name} (date,Expenses)
                    VALUES (%s,%s)
                    ON DUPLICATE KEY UPDATE
                    Expenses = VALUES(Expenses) 
                """
                insert_values = (
                    current_date.strftime("%Y-%m-%d"),  
                    final_expense
                    )
                
                try:
                    cursor.execute(insert_query, insert_values)
                    db_connection.commit()

                    # Get the ID of the last inserted row
                    last_inserted_id = cursor.lastrowid

                    # Get the number of affected rows
                    num_affected_rows = cursor.rowcount

                    print(f"Data inserted successfully. Last Inserted ID: {last_inserted_id}, Affected Rows: {num_affected_rows}")

                    post_transaction.Add_Transaction(db_host, db_user, db_password, db_name, current_date, "Checking_Account", note, amount, "Expense", sub_category,Bank_verified)
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                
            else:
                print(f"No expense found for {current_date}")
            # Add 1 month to the original date
            new_date = current_date + relativedelta(months=1)
            current_date = new_date
        
        
        checking_account_update.Update_Checking_account(db_host, db_user,db_password,db_name,table_name,year)
        # Commit the changes and close the connection
        db_connection.commit()
        cursor.close()
    