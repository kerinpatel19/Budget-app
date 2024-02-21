import mysql.connector
from Refresh_db.update_checking import update_checking_account
from Refresh_db.update_saveings import Update_saveings_account
from Refresh_db.update_bailout import Update_bailout_account

update_data_checking = update_checking_account
update_date_saveings = Update_saveings_account
update_date_bailout = Update_bailout_account
class StartBalance:
    def add_starting_balance(self, db_host, db_user, db_password, db_name, table_name, year, checking_account, bail_out, savings):
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

        inserted = False

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

            print(f"Data inserted successfully. Last Inserted ID: {last_inserted_id}, Affected Rows: {num_affected_rows}")
            print(current_year)
           # Correct method names here
            update_data_checking.update_Checking_account(db_host, db_user, db_password, db_name, table_name, current_year)
            update_date_saveings.update_Saveing_account(db_host, db_user, db_password, db_name, table_name, current_year)
            update_date_bailout.update_bailout_account(db_host, db_user, db_password, db_name, table_name, current_year)
            inserted = True

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and connection in a finally block
            cursor.close()
            db_connection.close()
            
       