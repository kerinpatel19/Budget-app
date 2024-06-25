import mysql.connector
from Refresh_db import update_all_accounts
from Ledger.Post_transaction import Add_Transaction

update = update_all_accounts.update_all_accounts()
post_transaction = Add_Transaction()
class StartBalance:
    def add_starting_balance(self, db_host, db_user, db_password, db_name, year, checking_account, bail_out, savings,Bank_verified):
        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        cursor = db_connection.cursor()
        
        # Get start date
        current_year = int(year)
        last_year = current_year - 1
        start_date = f"{last_year}-12-31"
        table_name = f"budget{current_year}"

        # Construct and execute the INSERT query
        insert_query = f"""
            INSERT INTO {table_name} (date, Checking_Account, Bail_Out, Savings)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            Checking_Account = VALUES(Checking_Account),
            Bail_Out = VALUES(Bail_Out),
            Savings = VALUES(Savings)
        """

        values = (start_date, checking_account, bail_out, savings)

        

        try:

            
            cursor.execute(insert_query, values)
            print(f"table_name before insert: {table_name}")
            cursor.execute(insert_query, values)
            db_connection.commit()
            print(f"table_name after insert: {table_name}")

            # Get the ID of the last inserted row
            last_inserted_id = cursor.lastrowid
            # Get the number of affected rows
            num_affected_rows = cursor.rowcount

            Message = (f"Data inserted successfully. Last Inserted ID: {last_inserted_id}, Affected Rows: {num_affected_rows}")
            print(Message)
            # Correct method names here
            
            update.Update_all_accounts(db_host, db_user,db_password,db_name,table_name,year)
            post_transaction.Add_Transaction(db_host, db_user, db_password, db_name, start_date, "Checking_Account", "Starting balance", checking_account, "Internal","Internal",Bank_verified)
            post_transaction.Add_Transaction(db_host, db_user, db_password, db_name, start_date, "Savings_Account", "Starting balance", savings, "Internal","Internal",Bank_verified)
            post_transaction.Add_Transaction(db_host, db_user, db_password, db_name, start_date, "Bailout_Account", "Starting balance", bail_out, "Internal","Internal",Bank_verified)
        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and connection in a finally block
            cursor.close()
            db_connection.close()
            return Message
