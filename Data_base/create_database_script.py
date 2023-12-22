from datetime import datetime, timedelta
import mysql.connector
import sys

## last ran successfully on 11/25/2023

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
        database_name = f"Database{num_year}"

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

def populate_single_table(database_name, year, db_host, db_user, db_password):
    current_year = int(year)
    # Establish a connection to MySQL
    db_connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=database_name
    )
    cursor = db_connection.cursor()

    # Define the column names and data types for the budget table
    columns = [
        "DATE DATE PRIMARY KEY",
        "Checking_Account DECIMAL(10, 2)",
        "Bail_Out DECIMAL(10, 2)",
        "Savings DECIMAL(10, 2)",
        "Transfer DECIMAL(10, 2)",
        "Income DECIMAL(10, 2)",
        "Expenses DECIMAL(10, 2)",
        "Note VARCHAR(255)",
        "CATEGORY VARCHAR(255)",
    ]

    # Create a single table for the year
    table_name = f"Yearly_budget"
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {', '.join(columns)}
    )
    """
    cursor.execute(create_table_query)
    db_connection.commit()
    start_data_query = f"""
    INSERT INTO {table_name} (DATE, Checking_Account, Bail_Out, Savings, Transfer, Income, Expenses, Note, CATEGORY) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    last_year = current_year - 1
    starting_date = f"{last_year}-12-31"
    data = (starting_date,100.0, 0.00, 0.00, 0.00, 0.00, 0.00, 'null', 'null')

    cursor.execute(start_data_query, data)
    # Populate the yearly table with dates
    for month in range(1, 13):
        # Get the number of days in the current month
        days_in_month = (datetime(current_year, month, 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        insert_data_query = f"""
        INSERT INTO {table_name} (DATE, Checking_Account, Bail_Out, Savings, Transfer, Income, Expenses, Note, CATEGORY) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = (0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 'null', 'null')

        # Generate a list of dates for the current month
        dates = [datetime(current_year, month, day).date() for day in range(1, days_in_month.day + 1)]

        # Insert dates into the table
        for date in dates:
            cursor.execute(insert_data_query, (date,) + data)
    
    posted_transaction_months = ["posted_transaction"]

    posted_transaction_columns = ["DATE DATE", "Amount DECIMAL(10, 2)", "Note VARCHAR(255)","CATEGORYS VARCHAR(255)"]

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
    
    table_name1 = 'Pending_transactions'
    pending_columns = [
        "TRANSACTION_DATE DATE",
        "NOTE VARCHAR(255)",
        "AMOUNT DECIMAL(10, 2)",
        "CATEGORYS VARCHAR(255)"
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

    # Create the Categorys table
    create_table_query5 = f"CREATE TABLE IF NOT EXISTS {table_name2.lower()} ({', '.join(category_columns)})"
    cursor.execute(create_table_query5)

    categorys = [
        "Income",
        "Outgoing",
        "Transfer",
        "Fixed Expense",
        "Going out",
        "School",
        "Food",
        "Other"
    ]

    for category in categorys:
        insert_data_query_cat = f"""
        INSERT INTO {table_name2.lower()} (Name) 
        VALUES (%s)
        """
        cursor.execute(insert_data_query_cat, (category,))
    # Commit changes and close the connection
    db_connection.commit() 
    # Close the cursor and connection
    cursor.close()
    db_connection.close()
    print("dates added")
    

def create_database_main(host, user, password, year):
    """
    The function `create_database_main` creates a MySQL database with a name based on the input year,
    using the provided host, user, and password.
    
    :param host: The `host` parameter is the hostname or IP address of the MySQL server where you want
    to create the database
    :param user: The "user" parameter is the username used to connect to the MySQL server. It is
    typically the username associated with the MySQL account that has the necessary privileges to create
    databases
    :param password: The password parameter is the password used to authenticate the user when
    connecting to the MySQL server
    :param year: The "year" parameter is the year for which you want to create the database. It is used
    to generate the name of the database by appending the year to the string "Database". For example, if
    the year is 2022, the name of the database will be "Database2022"
    """
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
    populate_single_table(name, year, host, user, password)

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
