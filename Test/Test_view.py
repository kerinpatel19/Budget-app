from Output_data.view_monthly_budget import view_budget

View_budget = view_budget()

db_host = 'localhost'
db_user = 'root'
db_password = 'Panna4120@'
db_name = "test"
From_account = "Checking_Account"
To_account = 'Savings'
start_date = "2023-02-21"
note = "test"
amount = 100.00

View_budget.view_Budget(db_host, db_user, db_password, db_name, start_date)
        