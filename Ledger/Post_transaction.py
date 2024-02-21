import mysql.connector
from datetime import datetime, timedelta

class Add_Transaction:
    @classmethod
    
    def Add_Transaction(cls, db_host, db_user, db_password, database_name, TransactionDate, Account, Note, Amount, Category, Sub_Category):
        
        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=database_name
        )
        cursor = db_connection.cursor()
        
        # Check the type of TransactionDate
        if isinstance(TransactionDate, datetime):
            current_date = TransactionDate  # If it's already a datetime object, use it directly
        else:
            current_date = datetime.strptime(TransactionDate, '%Y-%m-%d')
            
        # Extract the year
        year = current_date.year

        table_name = f"Posted_transactions_{year}"
        
        
        insert_data_query = f"""
            INSERT INTO {table_name} (TransactionDate, Account, Note, Amount, Category, Sub_Category) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """

        data = (TransactionDate, Account,Note, Amount, Category, Sub_Category)
        
        try:
                    cursor.execute(insert_data_query, data)
                    db_connection.commit()

                    # Get the ID of the last inserted row
                    last_inserted_id = cursor.lastrowid

                    # Get the number of affected rows
                    num_affected_rows = cursor.rowcount

                    print(f"Data inserted successfully. Last Inserted ID: {last_inserted_id}, Affected Rows: {num_affected_rows}")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        
        # Close the cursor and connection
        cursor.close()
        db_connection.close()