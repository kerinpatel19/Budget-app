from Output_data.view_expense_by_date import view_Expense

View_Expense = view_Expense()

db_host = 'localhost'
db_user = 'root'
db_password = 'Panna4120@'
db_name = "test"
lookup_date = "2023-02-21"

View_Expense.view_expense(db_host, db_user, db_password, db_name, lookup_date)
        