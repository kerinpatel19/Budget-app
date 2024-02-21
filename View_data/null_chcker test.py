from datetime import datetime, timedelta
import mysql.connector

db_host = 'localhost'
db_user = 'root'
db_password = 'Panna4120@'
db_name = "test"
table_name = "Budget2024"
start_date = '2023-12-31'
year = "2024"


cell = "'null'"

# Establish a connection to MySQL
db_connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
cursor = db_connection.cursor()
# Establish a connection to MySQL

# Fetch the row
query = f"SELECT * FROM {table_name} WHERE date = %s"
cursor.execute(query, (start_date,))
row = cursor.fetchone()

print(row)






# close the connection
cursor.close()


