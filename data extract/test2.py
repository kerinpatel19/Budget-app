from datetime import datetime
import mysql.connector

db_host = 'localhost'
db_user = 'root'
db_password = 'Panna4120@'

def Add_expense(Note, Amount, category, db_name):
    # Establish a connection to MySQL
    db_connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = db_connection.cursor()

    # Get the current date
    Transaction_date = datetime.now().date()

    # Construct the data tuple
    data = (Transaction_date, Note, Amount, category)

    # Construct the SQL query for inserting a new expense
    insert_data_query = """
    INSERT INTO pending_transactions (Transaction_date, Note, Amount, category) 
    VALUES (%s, %s, %s, %s)
    """

    try:
        # Execute the INSERT query with the provided values
        cursor.execute(insert_data_query, data)

        # Commit the changes to the database
        db_connection.commit()

        print("Expense added successfully!")

    except Exception as e:
        # Handle any errors that may occur during the insertion
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        db_connection.close()

if __name__ == "__main__":
    data_base_name = "Database2023"
    Note = "test"
    Amount = 10.0
    category = "Income"

    Add_expense(Note, Amount, category, data_base_name)
