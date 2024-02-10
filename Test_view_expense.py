from Output_data.view_monthly_budget import view_budget

View_budget = view_budget()

db_host = 'localhost'
db_user = 'root'
db_password = 'Panna4120@'
db_name = "test"
month_name = "January"
year = 2023

View_budget.view_Budget(db_host, db_user, db_password, db_name, month_name, year)  

