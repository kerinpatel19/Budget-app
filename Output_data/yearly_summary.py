import mysql.connector
from datetime import datetime
import calendar

class Get_summary:
    @classmethod
    def get_month_data(cls, db_host, db_user, db_password, db_name, year):
        
        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = db_connection.cursor()
        table_name = f"Budget{year}"
        return_list = []
        
        for month in range(1, 13):
            # Get the number of days in the month
            last_day = calendar.monthrange(year, month)[1]  # [1] to get the last day
            
            # Create a date object for the last day of the month
            date = datetime(year, month, last_day).strftime('%Y-%m-%d')
            try:
                select_query = f"""
                    SELECT Checking_Account,Bail_Out,Savings
                    FROM {table_name}
                    WHERE DATE = %s
                """
                cursor.execute(select_query,(date,))
                
                # Fetch all the tables
                rows = cursor.fetchall()
                
                # Print the table names
                for row in rows:
                    Checking = float(row[0])
                    bail_out = float(row[1])
                    saving = float(row[2])
                    
                    list_format = [month,Checking,bail_out,saving]
                    return_list.append(list_format)

            except mysql.connector.Error as err:
                print(f"Error: {err}")


        # Close the cursor and connection
        cursor.close()
        db_connection.close()

        return return_list


