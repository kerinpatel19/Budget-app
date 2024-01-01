from Input_data.Create_transfer import Transfer_money

add_expense = Transfer_money()

db_host = 'localhost'
db_user = 'root'
db_password = 'Panna4120@'
db_name = "test"
From_account = "Checking_Account"
To_account = 'Savings'
Transfer_date = "2023-02-21"
note = "test"
amount = 100.00

add_expense.Create_Transfer(db_host, db_user, db_password, db_name, From_account, To_account, Transfer_date, note, amount)
        
        
        