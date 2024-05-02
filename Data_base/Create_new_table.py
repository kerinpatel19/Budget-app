import mysql.connector
from datetime import datetime, timedelta

class Create_table:
    @classmethod
    def populate_single_table( cls, db_host, db_user, db_password, database_name, table_name,year):
        current_year = int(year)
        status = False
        try:
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
                "Bail_Out_AJC DECIMAL(10, 2)",
                "Savings DECIMAL(10, 2)",
                "Savings_AJC DECIMAL(10, 2)",
                "Transfer_Out DECIMAL(10, 2)",
                "Transfer_In DECIMAL(10, 2)",
                "Income DECIMAL(10, 2)",
                "Expenses DECIMAL(10, 2)"
            ]

            # Create a single table for the year
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {', '.join(columns)}
            )
            """
            cursor.execute(create_table_query)
            db_connection.commit()
            start_data_query = f"""
            INSERT INTO {table_name} (DATE, Checking_Account, Bail_Out, Bail_Out_AJC, Savings, Savings_AJC, Transfer_Out, Transfer_In, Income, Expenses) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            last_year = current_year - 1
            starting_date = f"{last_year}-12-31"
            data = (starting_date,0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00)

            cursor.execute(start_data_query, data)
            # Populate the yearly table with dates
            for month in range(1, 13):
                # Get the number of days in the current month
                days_in_month = (datetime(current_year, month, 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)

                insert_data_query = f"""
                INSERT INTO {table_name} (DATE, Checking_Account, Bail_Out, Bail_Out_AJC, Savings, Savings_AJC, Transfer_Out, Transfer_In, Income, Expenses) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                data = (0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00)

                # Generate a list of dates for the current month
                dates = [datetime(current_year, month, day).date() for day in range(1, days_in_month.day + 1)]

                # Insert dates into the table
                for date in dates:
                    cursor.execute(insert_data_query, (date,) + data)
            
            # Define the column names and data types for the budget table
            columns_posted = [
                "ID int AUTO_INCREMENT PRIMARY KEY",
                "TransactionDate DATE",
                "Account VARCHAR(255)",
                "Note  VARCHAR(255)",
                "Amount DECIMAL(10, 2)",
                "Category VARCHAR(255)",
                "Sub_Category VARCHAR(255)",
                "Bank_verified VARCHAR(255)"
            ]
            table_name_posted = f"Posted_transactions_{year}"
            # Create a single table for the year
            create_table_query_2 = f"""
            CREATE TABLE IF NOT EXISTS {table_name_posted} (
                {', '.join(columns_posted)}
            )
            """
            cursor.execute(create_table_query_2)
            db_connection.commit()
            
            table_name2 = 'categories'
            category_columns = [
                "ID int AUTO_INCREMENT PRIMARY KEY",
                "Category VARCHAR(255)",
                "Sub_Category VARCHAR(255)"
            ]

            # Create the Categorys table
            create_table_query5 = f"CREATE TABLE IF NOT EXISTS {table_name2.lower()} ({', '.join(category_columns)})"
            cursor.execute(create_table_query5)
            db_connection.commit()
            
            categories = [
                ("Income", "Income"),
                ("Income", "Tax Refund"),
                ("Income", "Refund"),
                ("Transfer", "In Transfer"),
                ("Transfer", "Out Transfer"),
                ("Expense", "Wants - Expense"),
                ("Expense", "Needs - Expense"),
                ("Expense", "Fixed Expense"),
                ("Expense", "subscription"),
                ("Expense", "School"),
                ("Expense", "Takeout - Food"),
                ("Expense", "Grocery - Food"),
                ("Expense", "Taxes"),
                ("Expense", "Other")
            ]

            for main_category, sub_category in categories:
                insert_data_query_cat = f"""
                INSERT INTO {table_name2.lower()} (Category, Sub_Category) 
                VALUES (%s, %s)
                """
                cursor.execute(insert_data_query_cat, (main_category, sub_category))
                db_connection.commit()
            status = True
            
            return status
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return status
        finally:
            # Close the cursor and connection
            cursor.close()
            db_connection.close()
            