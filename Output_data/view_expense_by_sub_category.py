import mysql.connector
from datetime import datetime, timedelta

class view_Expense:
    @classmethod
    def view_expense(cls, db_host, db_user, db_password, db_name, lookup_date, sub_catogeiors):
        
        look_up_date = datetime.strptime(lookup_date, '%Y-%m-%d').date()
    
        # Access the year attribute after ensuring start_date is a datetime object
        year = look_up_date.year
        table_name = f"Posted_transactions_{year}"
        
        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = db_connection.cursor()
        
        return_list = []
        
        try:
            select_query = f"SELECT * FROM `{table_name}` WHERE YEAR(TransactionDate) = %s AND MONTH(TransactionDate) = %s AND Sub_Category IN (%s)"

            cursor.execute(select_query, (look_up_date.year, look_up_date.month, sub_catogeiors))
    
            # Fetch all the rows
            rows = cursor.fetchall()
            
            for row in rows:
                date = datetime.strftime(row[1], '%Y-%m-%d')  # Format date as string
                note = row[3].strip()  # Clean the 'note' text by removing leading and trailing whitespace
                category = row[6].strip()  # Clean the 'Category' text by removing leading and trailing whitespace
                list_format = [
                    date,          # date
                    row[2],        # account
                    note,          # cleaned 'note'
                    float(row[4]), # amount
                    category       # cleaned 'Category'
                ]
                return_list.append(list_format)

            
                                
                
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            # Close the cursor and connection
            cursor.close()
            db_connection.close()
        if return_list is not None:
            return return_list
