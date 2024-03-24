import mysql.connector

db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Panna4120@',
    database="Database2023"
)
cursor = db_connection.cursor()

Insert = input("What would you like to insert : ")
table_name = "Categorys"
insert_data_query = f"""
INSERT INTO {table_name.lower()} (Name) 
VALUES (%s)
"""

try:
    cursor.execute(insert_data_query, (Insert,))
    db_connection.commit()

    # Get the ID of the last inserted row
    last_inserted_id = cursor.lastrowid

    # Get the number of affected rows
    num_affected_rows = cursor.rowcount

    print(f"Data inserted successfully. Last Inserted ID: {last_inserted_id}, Affected Rows: {num_affected_rows}")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    cursor.close()
    db_connection.close()