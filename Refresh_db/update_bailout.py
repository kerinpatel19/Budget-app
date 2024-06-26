from datetime import datetime, timedelta
import mysql.connector

class Update_bailout_account:
    @classmethod
    def Update_bailout_account(cls, db_host, db_user, db_password, db_name, table_name, year):
        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = db_connection.cursor()
        # Establish a connection to MySQL
        last_year = year - 1
        start_date = f"{last_year}-12-31"
        end_date = f"{year}-12-31"
        
        
        query = f"SELECT * FROM {table_name} WHERE date = %s"
        cursor.execute(query, (start_date,))

        # Fetch the row
        row = cursor.fetchone()
        daybefore_bailout_account = float(row[2])
        
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        current_date += timedelta(days=1)

        while current_date <= datetime.strptime(end_date, "%Y-%m-%d"):
            # Do something with the current date (e.g., print it)
            #print("Processing date:", current_date.strftime("%Y-%m-%d"))

            # Construct and execute the SQL query based on the current date
            query = f"SELECT * FROM {table_name} WHERE date = %s"
            cursor.execute(query, (current_date.strftime("%Y-%m-%d"),))

            
            # Fetch the row
            row = cursor.fetchone()
            Bail_Out_AJC = float(row[3])
            
            
            Insert_bailout_account = daybefore_bailout_account + Bail_Out_AJC
            
            # Construct and execute the INSERT query
            insert_query = f"""
                INSERT INTO {table_name} (date,Bail_Out)
                VALUES (%s,%s)
                ON DUPLICATE KEY UPDATE
                Bail_Out = VALUES(Bail_Out)
                
            """
            insert_values = (
            current_date.strftime("%Y-%m-%d"),  # Replace with the actual date value
            Insert_bailout_account,
            )
            
            daybefore_bailout_account = Insert_bailout_account
            try:
                cursor.execute(insert_query, insert_values)
                db_connection.commit()

                # Get the ID of the last inserted row
                last_inserted_id = cursor.lastrowid

                # Get the number of affected rows
                num_affected_rows = cursor.rowcount

                #print(f"Data inserted successfully. Last Inserted ID: {last_inserted_id}, Affected Rows: {num_affected_rows}")

            except mysql.connector.Error as err:
                print(f"Error: {err}")
            # Move to the next day
            current_date += timedelta(days=1)

        # Commit the changes and close the connection
        db_connection.commit()
        cursor.close()
        print("bail out account updated")
        
        
        