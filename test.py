from Output_data.get_sub_category import Get_sub_category

Get_Sub_category = Get_sub_category()

db_host = 'localhost'
db_user = 'root'
db_password = 'Panna4120@'
db_name = "test"
From_account = "Checking_Account"
To_account = 'Savings'
start_date = "2023-02-21"
note = "test"
amount = 100.00

return_list = Get_Sub_category.Get_Sub_Category(db_host, db_user, db_password, db_name)

print(return_list)
        