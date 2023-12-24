import mysql.connector
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from Ledger.Post_transaction import Add_Transaction
from Refresh_db.update_checking import update_checking_account


post_transaction = Add_Transaction()
Update_account = update_checking_account()

class Add_Income:
    @classmethod
    
    def Add_income(cls, db_host, db_user, db_password, db_name, Income_date, note, amount, Category):
        # Convert start_date to a datetime object if it's a string
        if isinstance(Income_date, str):
            Income_date = datetime.strptime(Income_date, '%Y-%m-%d')

        # Access the year attribute after ensuring start_date is a datetime object
        year = Income_date.year
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
        cursor.execute(query, (Income_date,))
        row = cursor.fetchone()

        if row is not None:
            # Check if 'Income' column (at index 8) is 'null' and handle accordingly
            income_index = 8
            current_income = 0.00 if row[income_index] == 'null' else float(row[income_index])

            final_income = current_income + amount

            insert_query = f"""
                INSERT INTO {table_name} (date,Income)
                VALUES (%s,%s)
                ON DUPLICATE KEY UPDATE
                Income = VALUES(Income) 
            """
            insert_values = (
                Income_date.strftime("%Y-%m-%d"),  
                final_income
                )
            
            try:
                cursor.execute(insert_query, insert_values)
                db_connection.commit()

                # Get the ID of the last inserted row
                last_inserted_id = cursor.lastrowid

                # Get the number of affected rows
                num_affected_rows = cursor.rowcount

                print(f"Data inserted successfully. Last Inserted ID: {last_inserted_id}, Affected Rows: {num_affected_rows}")

                post_transaction.Add_Transaction(db_host, db_user, db_password, db_name, Income_date, "Checking_Account", note, amount, Category)
            except mysql.connector.Error as err:
                print(f"Error: {err}")
            
        else:
            print(f"No expense found for {Income_date}")
        Update_account.update_Checking_account(db_host, db_user,db_password,db_name,table_name,year)
        
        