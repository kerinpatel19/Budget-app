import mysql.connector
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from Ledger.Post_transaction import Add_Transaction
from Refresh_db.update_checking import update_checking_account
from Refresh_db.update_saveings import Update_saveings_account
from Refresh_db.update_bailout import Update_bailout_account

post_transaction = Add_Transaction()
checking_account_update = update_checking_account()
saveing_account_update = Update_saveings_account()
bailout_account_update = Update_bailout_account()

class view_budget:
    @classmethod
    def view_Budget(cls, db_host, db_user, db_password, db_name, start_date ):
        
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        # get the nd date for the loop 
        end_date = start_date + timedelta(days=31)
    
        # Access the year attribute after ensuring start_date is a datetime object
        year = start_date.year
        table_name = f"Budget{year}"
        
        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = db_connection.cursor()
        current_date = start_date
        
        
        while current_date < end_date:
            
            # Fetch the row
            query = f"SELECT * FROM {table_name} WHERE date = %s"
            cursor.execute(query, (current_date,))
            row = cursor.fetchone()

            if row is not None:
                print(f"[{row[0]}] checking account :-{row[1]} Bail out :-{row[2]} Savings :- {row[4]} Transfer out {row[6]} Transfer In {row[7]} Income {row[8]} Expense {row[9]}")
                current_date = current_date + timedelta(days=1)
            else : 
                print("Error")
                break
