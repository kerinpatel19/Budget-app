import mysql.connector
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from Ledger.Post_transaction import Add_Transaction
from Refresh_db.update_checking import update_checking_account


post_transaction = Add_Transaction()
Update_account = update_checking_account()


class Add_Expense:
    @classmethod
    
    def Add_expense(cls, db_host, db_user, db_password, db_name, Expense_date, note, amount, Sub_Category,Bank_verified):
        # Convert start_date to a datetime object if it's a string
        if isinstance(Expense_date, str):
            Expense_date = datetime.strptime(Expense_date, '%Y-%m-%d')

        # Access the year attribute after ensuring start_date is a datetime object
        year = Expense_date.year
        table_name = f"Budget{year}"
        

        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = db_connection.cursor()
        
        # Fetch the row
        query = f"SELECT * FROM {table_name} WHERE date = %s"
        cursor.execute(query, (Expense_date,))
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
                Expense_date.strftime("%Y-%m-%d"),  
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

                post_transaction.Add_Transaction(db_host, db_user, db_password, db_name, Expense_date, "Checking_Account", note, amount, "Expense", Sub_Category,Bank_verified)
            except mysql.connector.Error as err:
                print(f"Error: {err}")
            finally :
                db_connection.commit()
                cursor.close()
        else:
            print(f"No expense found for {Expense_date}")

        