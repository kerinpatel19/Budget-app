import mysql.connector

class delete_year:
    @classmethod
    def delete_year_table(cls,db_host, db_user, db_password, db_name,year):
        
        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = db_connection.cursor()
        
        
        try:
            # Construct the table name based on the provided year
            Budget_table_name = f"Budget_{year}"
            Posted_table_name = f"Posted_transactions_{year}"
            # Drop the table
            drop_query = f"DROP TABLE IF EXISTS {Budget_table_name}"
            cursor.execute(drop_query)
            drop_query = f"DROP TABLE IF EXISTS {Posted_table_name}"
            cursor.execute(drop_query)
            db_connection.commit()

            return True

        except mysql.connector.Error as err:
            db_connection.rollback()
            print(f"Error: {err}")
            return False

        finally:
            # Close the cursor and connection
            cursor.close()
            db_connection.close()

