from Input_data.Add_fixed_expense import Add_fixed_expense

add_expense = Add_fixed_expense()

db_host = 'localhost'
db_user = 'root'
db_password = 'Panna4120@'
db_name = "test"
table_name = "Budget2023"
start_date = "2023-02-20"
year = "2023"
amount = 10.00


add_expense.Add_Fixed_expense(db_host, db_user, db_password, db_name,table_name, start_date, year, amount) 