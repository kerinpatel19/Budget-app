from controller import Controller

controller = Controller()

db_host, db_user, db_password, db_name = controller.db_connecter()
row_ID = 21
row_date = "2023-12-31"
year = 2024
name_list = controller.delete_expense_row(row_ID, row_date,year)

print(name_list)