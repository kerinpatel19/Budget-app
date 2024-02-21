import mysql.connector

class Create_data_base:
    
    def create_database_main(self, host, user, password, name):
        try:
            # Establish a connection to MySQL
            db_connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            cursor = db_connection.cursor()

            # Create the target database directly
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {name}")
            print(f"Database {name} created successfully.")

            db_connection.commit()
            # Close the cursor and connection
            cursor.close()
            db_connection.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
