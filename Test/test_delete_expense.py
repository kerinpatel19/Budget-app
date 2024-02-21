from Remove_data.Delete_expense import Delete_expense

delete_expense = Delete_expense()

db_host = 'localhost'
db_user = 'root'
db_password = 'Panna4120@'
db_name = "test"
row_date = "2023-03-10"
row_ID = 2

delete_expense.delete_expense(db_host, db_user, db_password, db_name, row_ID, row_date)
        