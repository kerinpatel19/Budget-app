import mysql.connector
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from Refresh_db.update_checking import update_checking_account
from Refresh_db.update_saveings import Update_saveings_account
from Refresh_db.update_bailout import Update_bailout_account

checking_account_update = update_checking_account()
saveing_account_update = Update_saveings_account()
bailout_account_update = Update_bailout_account()

class view_budget:
    @classmethod
    def view_Budget(cls, db_host, db_user, db_password, db_name, month_name, year):
        # Convert month name to its corresponding number
        month_number = int(datetime.strptime(month_name, "%B").month)
        
        # Calculate the first date of the month
        first_date_of_month = datetime(year, month_number, 1)
        
        # Calculate the last date of the month
        next_month = first_date_of_month.replace(day=28) + timedelta(days=4)
        last_date_of_month = next_month - timedelta(days=next_month.day)
        
        start_date = first_date_of_month
        end_date = last_date_of_month
        
        # Access the year attribute after ensuring start_date is a datetime object
        table_name = f"Budget{year}"
        
        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = db_connection.cursor()
        return_list = []
        current_date = start_date

        while current_date <= end_date:
            
            lookup_date = current_date.strftime("%Y-%m-%d")
            try:
                # Fetch the row
                query = f"SELECT * FROM {table_name} WHERE date = %s"
                cursor.execute(query,(lookup_date,))
                row = cursor.fetchone()

                if row is not None:
                    #print(f"[{row[0]}] checking account :-{row[1]} Bail out :-{row[2]} Savings :- {row[4]} Transfer out {row[6]} Transfer In {row[7]} Income {row[8]} Expense {row[9]}")
                    list_format = [
                        lookup_date, #date
                        f"$ {float(row[1]):,.2f}", #checking
                        f"$ {float(row[2]):,.2f}", #bail out
                        f"$ {float(row[4]):,.2f}", #saving
                        f"$ {float(row[6]):,.2f}", #transfer out
                        f"$ {float(row[7]):,.2f}", #transfer in 
                        f"$ {float(row[8]):,.2f}", #income
                        f"$ {float(row[9]):,.2f}" #expense
                    ]
                    return_list.append(list_format)
                
            except Exception as e:
                print("Error executing query:", e)
                return ["No data found"]

            
            current_date = current_date + timedelta(days=1)
        
        return return_list