# save this script as create_database_script.py
from datetime import datetime, timedelta
import mysql.connector
import sys

## last ran successfullly on 11/25/2023

def check_if_available(host, user, password, year):
    try:
        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = db_connection.cursor()
        num_year = str(year)
        database_name =  num_year + "Database"
        
        # Check if the database exists
        cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")

        # Fetch the result
        result = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        db_connection.close()

        # Return True if the database exists, False otherwise
        return bool(result)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
def populate_months(database_name, year, db_host, db_user, db_password):
    current_year = int(year)
    # Establish a connection to MySQL
    db_connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=database_name
    )
    cursor = db_connection.cursor()

    # Define a dictionary of month names and corresponding numbers
    months = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }

    # Define the column names and data types for the budget table
    columns = [
        "DATE DATE",
        "Checking_Account DECIMAL(10, 2)",
        "Bail_Out DECIMAL(10, 2)",
        "Savings DECIMAL(10, 2)",
        "Transfer DECIMAL(10, 2)",
        "Income DECIMAL(10, 2)",
        "Expenses DECIMAL(10, 2)",
        "Note VARCHAR(255)",
        "CATEGORY VARCHAR(255)",
    ]
   
    # Create tables for each month
    for month in months:
        table_name_lower = month.lower()

        create_table_query1 = f"""
        CREATE TABLE IF NOT EXISTS {table_name_lower} (
            {', '.join(columns)}
        )
        """

        cursor.execute(create_table_query1)
    db_connection.commit()

    # Populate each monthly table with dates
    for month in months:
        # Get the number of days in the current month
        days_in_month = (datetime.strptime(month, "%B").replace(year=2023, day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        # Define the INSERT query to populate the table
        insert_data_query = f"""
        INSERT INTO {month} (DATE, Checking_Account, Bail_Out, Savings, Transfer, Income, Expenses) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        

        data = (0.00, 0.00, 0.00, 0.00, 0.00, 0.00)

        # Generate a list of dates for the current month
        dates = [datetime(2023, datetime.strptime(month, "%B").month, day).date() for day in range(1, days_in_month.day + 1)]

        # Insert dates into the table
        for date in dates:
            cursor.execute(insert_data_query, (date,)+data)
            #cursor.execute(insert_data_query2a, data)

    posted_transaction_months = ["posted_transaction_january",
                                "posted_transaction_february",
                                "posted_transaction_march", 
                                "posted_transaction_april", 
                                "posted_transaction_may", 
                                "posted_transaction_june", 
                                "posted_transaction_july", 
                                "posted_transaction_august", 
                                "posted_transaction_september", 
                                "posted_transaction_october", 
                                "posted_transaction_november", 
                                "posted_transaction_december"]

    posted_transaction_columns = ["DATE DATE", "Amount DECIMAL(10, 2)", "Note VARCHAR(255)"]

    # Create tables for posted transactions
    for posted_transaction_month in posted_transaction_months:
        posted_transaction_month_lower = posted_transaction_month.lower()
        create_table_query2 = f"""
        CREATE TABLE IF NOT EXISTS {posted_transaction_month_lower} (
            {', '.join(posted_transaction_columns)}
        )
        """

        cursor.execute(create_table_query2)

    db_connection.commit()

    table_name = 'Fixed_Expenses'
    fixed_expense_columns = [
        "Transaction_date DATE",
        "Note VARCHAR(255)",
        "Amount DECIMAL(10, 2)",
        "category VARCHAR(255)"
    ]

    # Create the Fixed Expenses table
    create_table_query4 = f"CREATE TABLE IF NOT EXISTS {table_name.lower()} ({', '.join(fixed_expense_columns)})"
    cursor.execute(create_table_query4)

    # Commit changes and close the connection
    db_connection.commit() 
    
    table_name1 = 'pending_transactions'
    pending_columns = [
        "Transaction_date DATE",
        "Note VARCHAR(255)",
        "Amount DECIMAL(10, 2)",
        "category VARCHAR(255)"
    ]

    # Create the Pending Transactions table
    create_table_query3 = f"CREATE TABLE IF NOT EXISTS {table_name1.lower()} ({', '.join(pending_columns)})"
    cursor.execute(create_table_query3)
    
    # Commit changes and close the connection
    db_connection.commit()
    
    table_name2 = 'Categorys'
    category_columns = [
        "Name VARCHAR(255)",
    ]

    # Create the Fixed Expenses table
    create_table_query5 = f"CREATE TABLE IF NOT EXISTS {table_name2.lower()} ({', '.join(category_columns)})"
    cursor.execute(create_table_query5)

    # Commit changes and close the connection
    db_connection.commit() 
    # Close the cursor and connection
    cursor.close()
    db_connection.close()


def create_database_main(host, user, password, year):
    name = f"Database{year}"
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
        # Define the list of month names 
    populate_months (name, year, host, user, password)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_database_script.py <year>")
        sys.exit(1)

    year_to_create = int(sys.argv[1])
    db_host = 'localhost'
    db_user = 'root'
    db_password = 'Panna4120@'

    if not check_if_available(db_host, db_user, db_password, year_to_create):
        create_database_main(db_host, db_user, db_password, year_to_create)
    else:
        print(f"Database {year_to_create} already exists.")
