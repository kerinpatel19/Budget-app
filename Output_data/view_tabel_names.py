import mysql.connector
from datetime import datetime

class View_table_names:
    @classmethod
    def View_all_table(cls, db_host, db_user, db_password, db_name):
        
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
            select_query = "SHOW TABLES"
            cursor.execute(select_query)
            
            # Fetch all the tables
            tables = cursor.fetchall()

            # Print the table names
            for table in tables:
                if "Budget" in table[0]:
                    return_list.append(table[0])

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            # Close the cursor and connection
            cursor.close()
            db_connection.close()
        
        if return_list:
            return return_list
        else:
            return ["No Tables"]

