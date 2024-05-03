import mysql.connector

class Update_expense_category:
    @classmethod
    def update_category(db_host, db_user, db_password, db_name,transaction_ID,transaction_date,new_category,year):
        
        # Establish a connection to MySQL
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = db_connection.cursor()
        
        
        try:
            # Construct the table name based on the provided year
            table_name = f"Posted_transactions_{year}"

            # Update the Sub_Category for the given transaction_ID
            update_query = f"UPDATE {table_name} SET Sub_Category = %s WHERE ID = %s AND TransactionDate = %s"
            cursor.execute(update_query, (new_category, transaction_ID,transaction_date))
            db_connection.commit()

            #return f"Sub_Category updated successfully for transaction ID {transaction_ID} in {table_name}."

        except mysql.connector.Error as err:
            db_connection.rollback()
            print(f"Error: {err}")
            #return f"Failed to update Sub_Category for transaction ID {transaction_ID} in {table_name}."

        finally:
            # Close the cursor and connection
            cursor.close()
            db_connection.close()

