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


class Transfer_money:
    @classmethod
    
    def Create_Transfer(cls, db_host, db_user, db_password, db_name, From_account, To_account, Transfer_date, note, amount):
        # Convert start_date to a datetime object if it's a string
        Category = "Transfer"
        if isinstance(Transfer_date, str):
            Transfer_date = datetime.strptime(Transfer_date, '%Y-%m-%d')

        # Access the year attribute after ensuring start_date is a datetime object
        year = Transfer_date.year
        table_name = f"Budget{year}"
        
        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = db_connection.cursor()
        
        # Fetch the row
        query = f"SELECT * FROM {table_name} WHERE date = %s"
        cursor.execute(query, (Transfer_date,))
        row = cursor.fetchone()

        if row is not None:
            
            
            bailout_ajc = float(row[3])
            saveing_ajc = float(row[5])
            transfer_out = float(row[6])
            transfer_in = float(row[7])
            
            if From_account == 'Checking_Account':
                if To_account == 'Bail_Out':
                    From_Account_amount = amount + transfer_out
                    From_name = "Transfer_Out"
                    Too_Account_amount = amount + bailout_ajc
                    Too_name = "Bail_Out_AJC"

                elif To_account == 'Savings':
                    From_Account_amount = amount + transfer_out
                    From_name = "Transfer_Out"
                    Too_Account_amount = amount + saveing_ajc
                    Too_name = "Savings_AJC"
                    
            elif From_account == 'Bail_Out':
                if To_account == 'Checking_Account':
                    From_Account_amount = -(amount)
                    From_name = "Bail_Out_AJC"
                    Too_Account_amount = amount + transfer_in
                    Too_name = "Transfer_In"
                    
                elif To_account == 'Savings':
                    From_Account_amount = -(amount)
                    From_name = "Bail_Out_AJC"
                    Too_Account_amount = amount + saveing_ajc
                    Too_name = "Savings_AJC"
                    
            elif From_account == 'Savings':
                if To_account == 'Checking_Account':
                    From_Account_amount = -(amount)
                    From_name = 'Savings_AJC'
                    Too_Account_amount = amount + transfer_in
                    Too_name = "Transfer_In"
                    
                elif To_account == 'Bail_Out':
                    From_Account_amount = -(amount)
                    From_name ="Savings_AJC"
                    Too_Account_amount = amount + bailout_ajc
                    Too_name = "Bail_Out_AJC"
            
            
            insert_query = f"""
                INSERT INTO {table_name} (DATE,{Too_name},{From_name})
                VALUES (%s,%s,%s)
                ON DUPLICATE KEY UPDATE
                {Too_name} = VALUES({Too_name}), 
                {From_name} = VALUES({From_name}) 
            """
            insert_values = (
                Transfer_date.strftime("%Y-%m-%d"),  
                Too_Account_amount,
                From_Account_amount
                )
            
            try:
                cursor.execute(insert_query, insert_values)
                db_connection.commit()

                # Get the ID of the last inserted row
                last_inserted_id = cursor.lastrowid

                # Get the number of affected rows
                num_affected_rows = cursor.rowcount

                print(f"Data inserted successfully. Last Inserted ID: {last_inserted_id}, Affected Rows: {num_affected_rows}")
                #from post
                post_transaction.Add_Transaction(db_host, db_user, db_password, db_name, Transfer_date, From_account, note, amount, "Transfer OUT")
                #too post
                post_transaction.Add_Transaction(db_host, db_user, db_password, db_name, Transfer_date, To_account, note, amount, "Transfer IN")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
            
        else:
            print(f"No expense found for {Transfer_date}")
        checking_account_update.Update_Checking_account(db_host, db_user,db_password,db_name,table_name,year)
        saveing_account_update.Update_Saveing_account(db_host, db_user,db_password,db_name,table_name,year)
        bailout_account_update.Update_bailout_account(db_host, db_user,db_password,db_name,table_name,year)
        
        