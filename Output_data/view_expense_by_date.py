import mysql.connector
from datetime import datetime, timedelta

class view_Expense:
    @classmethod
    def view_expense(cls, db_host, db_user, db_password, db_name, lookup_date):
        
        if isinstance(lookup_date, str):
            lookup_date = datetime.strptime(lookup_date, '%Y-%m-%d')
    
        # Access the year attribute after ensuring start_date is a datetime object
        year = lookup_date.year
        table_name = f"Posted_transactions_{year}"
        
        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = db_connection.cursor()
        
        try:
            # Construct and execute the SQL query with the date condition
            select_query = f"SELECT * FROM {table_name} WHERE TransactionDate = %s"
            cursor.execute(select_query, (lookup_date,))

            # Fetch all the rows
            rows = cursor.fetchall()

            # Display the results
            for row in rows:
                print(f"ID :-{row[0]} | Date :-{row[1]} | Account :-{row[2]} | Note :- {row[3]} | Amount :-{row[4]} | Category :-{row[5]}")
                
                
                
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            # Close the cursor and connection
            cursor.close()
            db_connection.close()
