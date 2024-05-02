import mysql.connector
from datetime import datetime, timedelta


class GetCategory:
    @classmethod
    def get_category(cls,db_host, db_user, db_password, db_name,Control_category):
        return_list = []
        
        table_name = f"categorys"
        
        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = db_connection.cursor()
        
        try:
            # Construct and execute the SQL query to select all distinct values from the Sub_Category column
            select_query = f"SELECT DISTINCT Sub_Category FROM {table_name} WHERE Category = %s"
            cursor.execute(select_query, (Control_category,))

            # Fetch all the rows
            rows = cursor.fetchall()

            # Display the results
            for row in rows:
                return_list.append(row[0])  # Assuming Sub_Category is the first (0-indexed) column
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            # Close the cursor and connection
            cursor.close()
            db_connection.close()
        return return_list
    
    
