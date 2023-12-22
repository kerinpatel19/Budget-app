from datetime import datetime, timedelta
import mysql.connector
import calendar

db_host = 'localhost'
db_user = 'root'
db_password = 'Panna4120@'

# Define custom names for each column
column_names = {
    "date": "| DATE",
    "checking_account": "| Checking_Account",
    "bail_out": "| Bail_Out",
    "savings": "| Savings",
    "transfer": "| Transfer",
    "income": "| Income",
    "expenses": "| Expenses",
    "note": "| Note",
    "category": "| CATEGORY |",
}
    
def View_budget(Month_key, db_name):
    # Establish a connection to MySQL
    db_connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = db_connection.cursor()
    
  
    # Input month as a string (e.g., "January")
    input_month = Month_key  # Replace with your desired month

    # Convert input month to its corresponding numeric value
    month_number = list(calendar.month_name).index(input_month.capitalize())

    # Get the number of days in the specified month and year (assuming a non-leap year)
    days_in_month = calendar.monthrange(2023, month_number)[1]

    # Iterate through each day of the month
    for day in range(1, days_in_month + 1):
        # Construct the primary key in the correct format (YYYY-MM-DD)
        your_primary_key = f"2023-{month_number:02d}-{day:02d}"

        # Execute the SELECT query
        query = "SELECT * FROM Yearly_budget WHERE date = %s"
        cursor.execute(query, (your_primary_key,))

        # Fetch the row
        row = cursor.fetchone()

        # Print the result with custom column names
        print(f"{column_names['date']}: {row[0]}, {column_names['checking_account']}: {row[1]}, {column_names['bail_out']}: {row[2]}, "
            f"{column_names['savings']}: {row[3]}, {column_names['transfer']}: {row[4]}, {column_names['income']}: {row[5]}, "
            f"{column_names['expenses']}: {row[6]}, {column_names['note']}: {row[7]}, {column_names['category']}: {row[8]}")
        line_break = 170
        i = 0
        while i < line_break:
            print("_",end="")
            i = i + 1
            
        print("")

    # Close the cursor and connection
    cursor.close()
    db_connection.close()



    
    
    
    
    
    
if __name__ == "__main__":
    
    month = "february"
    data_base_name = "Database2023"
    
    View_budget(month, data_base_name)