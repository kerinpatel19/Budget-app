import mysql.connector
from datetime import datetime, timedelta
from Refresh_db.update_all_accounts import update_all_accounts

Update_all_accounts = update_all_accounts()

class Delete_expense:
    @classmethod
    def delete_expense (cls, db_host, db_user, db_password, db_name, row_ID, row_date,year):
        
        if isinstance(row_date, str):
            row_date = datetime.strptime(row_date, '%Y-%m-%d')
    
        # Access the year attribute after ensuring start_date is a datetime object
        posted_table_name = f"Posted_transactions_{year}"
        budget_table_name = f"Budget{year}"
        
        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = db_connection.cursor()
        
        row_available = False
        delete_amount = 0.0
        
        #first we need to get the row from the posted tractions table
        try:
            # Construct and execute the SQL query with the date condition
            select_query = f"SELECT * FROM {posted_table_name} WHERE ID = %s"
            cursor.execute(select_query, (row_ID,))

            # Fetch all the rows
            rows = cursor.fetchall()
            # Display the results
            for row in rows:
                #print(f"ID :-{row[0]} | Date :-{row[1]} | Account :-{row[2]} | Note :- {row[3]} | Amount :-{row[4]} | Category :-{row[5]}")
                row_available = True
                delete_amount = float(row[4])
                account = row[2]
                category = row[5]
                
                
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        
        
        if row is not None:
        
            if row_available == True:
                #get the row from the budget table and update it 
                try:
                    # Construct and execute the SQL query with the date condition
                    select_query = f"SELECT * FROM {budget_table_name} WHERE DATE = %s"
                    row_date = row_date.date()
                    cursor.execute(select_query, (row_date,))
                    

                    # Fetch all the rows
                    rows = cursor.fetchall()
                    
                    
                    outer_tuple = rows[0]
                
                    
                    #print(f"[{row[0]}] checking account :-{row[1]} Bail out :-{row[2]} Savings :- {row[4]} Transfer out {row[6]} Transfer In {row[7]} Income {row[8]} Expense {row[9]}")
                    for row in rows:
            
                        transfer_out = float(row[6]) 
                        transfer_in = float(row[7])
                        income = float(row[8])
                        expense = float(row[9])
                        Bail_Out_AJC = float(row[3])
                        Savings_AJC = float(row[5])
                    
                        
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                
                insert_query = None
                insert_values = None
                if account == "Checking_Account":
                    if category == "Income":
                        if income >= delete_amount:
                            new_income = income - delete_amount
                            insert_query = f"""
                            INSERT INTO {budget_table_name} (date,Income)
                            VALUES (%s,%s)
                            ON DUPLICATE KEY UPDATE
                            Income = VALUES(Income) 
                            """
                            insert_values = (row_date,  new_income)
                    elif category == "Expense" or "Fixed_expense":
                        if expense >= delete_amount:
                            new_expense = expense - delete_amount
                            insert_query = f"""
                            INSERT INTO {budget_table_name} (date,Expenses)
                            VALUES (%s,%s)
                            ON DUPLICATE KEY UPDATE
                            Expenses = VALUES(Expenses) 
                            """
                            insert_values = (row_date,  new_expense)
                    elif category == "Transfer out":
                        if transfer_out >= delete_amount:
                            new_transfer_out = transfer_out - delete_amount
                            insert_query = f"""
                            INSERT INTO {budget_table_name} (date,Transfer_Out)
                            VALUES (%s,%s)
                            ON DUPLICATE KEY UPDATE
                            Transfer_Out = VALUES(Transfer_Out) 
                            """
                            insert_values = (row_date,  new_transfer_out)
                    elif category == "Transfer In":
                        if transfer_in >= delete_amount:
                            new_transfer_in = transfer_in - delete_amount
                            insert_query = f"""
                            INSERT INTO {budget_table_name} (date,Transfer_In)
                            VALUES (%s,%s)
                            ON DUPLICATE KEY UPDATE
                            Transfer_In = VALUES(Transfer_In) 
                            """
                            insert_values = (row_date,  new_transfer_in)
                            
                    try:
                        cursor.execute(insert_query, insert_values)
                        db_connection.commit()

                        # Get the ID of the last inserted row
                        last_inserted_id = cursor.lastrowid

                        # Get the number of affected rows
                        num_affected_rows = cursor.rowcount

                        print(f"Data inserted successfully. Last Inserted ID: {last_inserted_id}, Affected Rows: {num_affected_rows}")
                        
                    except mysql.connector.Error as err:
                        print(f"Error: {err}")     
                    
                    
                elif account == "Savings":
                    
                    if Savings_AJC > delete_amount:
                        
                        final_Savings_AJC = Savings_AJC - delete_amount
                        insert_query = f"""
                            INSERT INTO {budget_table_name} (date,Savings_AJC)
                            VALUES (%s,%s)
                            ON DUPLICATE KEY UPDATE
                            Savings_AJC = VALUES(Savings_AJC) 
                            """
                        insert_values = (row_date,  final_Savings_AJC)
                            
                        try:
                            cursor.execute(insert_query, insert_values)
                            db_connection.commit()

                            # Get the ID of the last inserted row
                            last_inserted_id = cursor.lastrowid

                            # Get the number of affected rows
                            num_affected_rows = cursor.rowcount

                            print(f"Data inserted successfully. Last Inserted ID: {last_inserted_id}, Affected Rows: {num_affected_rows}")
                            
                        except mysql.connector.Error as err:
                            print(f"Error: {err}") 
                
                elif account == "Bail_Out":
                    if Bail_Out_AJC > delete_amount:
                        final_Bail_Out_AJC = Bail_Out_AJC - delete_amount
                        insert_query = f"""
                            INSERT INTO {budget_table_name} (date,Bail_Out_AJC)
                            VALUES (%s,%s)
                            ON DUPLICATE KEY UPDATE
                            Bail_Out_AJC = VALUES(Bail_Out_AJC) 
                            """
                        insert_values = (row_date,  final_Bail_Out_AJC)
                            
                        try:
                            cursor.execute(insert_query, insert_values)
                            db_connection.commit()

                            # Get the ID of the last inserted row
                            last_inserted_id = cursor.lastrowid

                            # Get the number of affected rows
                            num_affected_rows = cursor.rowcount

                            print(f"Data inserted successfully. Last Inserted ID: {last_inserted_id}, Affected Rows: {num_affected_rows}")
                            
                        except mysql.connector.Error as err:
                            print(f"Error: {err}") 
                
            
                Update_all_accounts.Update_all_accounts(db_host, db_user,db_password,db_name,budget_table_name,year)

                try:
                    # Construct and execute the DELETE statement with the WHERE clause
                    delete_query = f"DELETE FROM {posted_table_name} WHERE id = %s"
                    cursor.execute(delete_query, (row_ID,))

                    # Commit the changes
                    db_connection.commit()

                    return(f"Transaction ID {row_ID} - Deleted")
                except mysql.connector.Error as err:
                    return(f"Error: {err}")
                    
        else:
            return(f"No expense found for {row_date}")
        