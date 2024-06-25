import mysql.connector
from datetime import datetime, timedelta
import calendar

class view_Expense:
    @classmethod
    def view_expense(cls, db_host, db_user, db_password, db_name, Start_date, sub_catogeiors):
        
        Start_date = datetime.strptime(Start_date, '%Y-%m-%d').date()
        year = Start_date.year
        month = Start_date.month
        table_name = f"Posted_transactions_{year}"
        
        
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = db_connection.cursor()
        
        return_list = []
        try:
            select_query = F"SELECT * FROM {table_name} WHERE YEAR(TransactionDate) = %s AND MONTH(TransactionDate) = %s AND Category = %s;"
            cursor.execute(select_query, (year, month ,sub_catogeiors))

            rows = cursor.fetchall()
            
            for row in rows:
                Id = row[0]
                date = row[1].strftime('%Y-%m-%d')
                note = row[3].strip()
                category = row[6].strip()
                bank_verified = row[7]
                
                list_format = [
                    Id,
                    date,
                    row[2],
                    note,
                    float(row[4]),
                    category,
                    bank_verified
                ]
                return_list.append(list_format)
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db_connection.close()
        
        return return_list
