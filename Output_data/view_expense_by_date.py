import mysql.connector
from datetime import datetime, timedelta

class view_Expense:
    @classmethod
    def view_expense(cls, db_host, db_user, db_password, db_name, lookup_date):
        
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
            # Construct and execute the SQL query with the date condition
            select_query = f"SELECT * FROM {table_name} WHERE TransactionDate = %s"
            cursor.execute(select_query, (look_up_date,))

            # Fetch all the rows
            rows = cursor.fetchall()

            # Display the results
            if len(rows) == 0:
                # No rows found for the given date
                return_list.append(["None available"])
            else:
                for row in rows:
                    list_format = [
                                row[1],  # date
                                row[2],  # account
                                row[3],  # note
                                float(row[4]),  # amount
                                row[5]]  # Category
                    return_list.append(list_format)
                    
                
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            # Close the cursor and connection
            cursor.close()
            db_connection.close()
        return return_list
