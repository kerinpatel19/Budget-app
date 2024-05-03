import mysql.connector
from datetime import datetime, timedelta

class GetCategoryAmount:
    @classmethod
    def get_category_amount(cls, db_host, db_user, db_password, db_name, start_date):
        try:
            # Establish a connection to MySQL
            db_connection = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            )
            cursor = db_connection.cursor()

            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            table_name = f"Posted_transactions_{start_date_dt.year}"

            # Calculate the end of the month
            if start_date_dt.month == 12:
                end_date = start_date_dt.replace(day=1, month=1, year=start_date_dt.year + 1)
            else:
                end_date = start_date_dt.replace(day=1, month=start_date_dt.month + 1)

            end_date -= timedelta(days=1)

            start_date_str = start_date_dt.strftime("%Y-%m-%d")
            end_date_str = end_date.strftime("%Y-%m-%d")

            # Construct and execute the SQL query to select Category and Amount for the given month and category
            select_query = f"""
                SELECT Sub_Category, SUM(Amount) AS TotalAmount
                FROM {table_name}
                WHERE TransactionDate >= %s
                AND TransactionDate <= %s
                GROUP BY Sub_Category
            """
            cursor.execute(select_query, (start_date_str, end_date_str))

            # Fetch all the rows
            rows = cursor.fetchall()

            # Construct the result list ["category - amount"]
            result_list = [[f"{row[0]}",f"{row[1]}"] for row in rows]
        
            return result_list

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

        finally:
            # Close the cursor and connection
            cursor.close()
            db_connection.close()

## Example usage
#db_host = "localhost"
#db_user = "root"
#db_password = "Panna4120@"
#db_name = "test"
#category = "Expense-Unsorted"
#start_date = "2024-12-01"
#
#result = GetCategoryAmount.get_category_amount(db_host, db_user, db_password, db_name, category, start_date)
#print(result)
#