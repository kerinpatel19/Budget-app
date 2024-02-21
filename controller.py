from datetime import datetime, timedelta
from Output_data import view_monthly_budget
from Output_data import view_expense_by_date
from Output_data import get_sub_category
from Input_data.Add_income import Add_Income
from Input_data.Add_expense import Add_Expense
from Input_data.Create_transfer import Transfer_money
from Input_data.Add_fixed_expense import Add_fixed_expense

class Controller:
    
    def __init__(self):
        self.view_budget = view_monthly_budget.view_budget()  # Instantiate the view_budget class
        self.find_expense_by_date = view_expense_by_date.view_Expense()
        self.add_income = Add_Income()
        self.add_expense = Add_Expense()
        self.Transfer = Transfer_money()
        self.add_fixed_expense = Add_fixed_expense()
        self.get_category = get_sub_category.Get_sub_category()
        
    def db_connecter(self):
        db_host = None
        db_user = None
        db_password = None
        db_name = None
        file_path = "/Users/kerinpatel/Desktop/Budget app/config.ingore/database_key.txt"
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    key, value = line.strip().split('=')
                    if key == 'DB_HOST':
                        db_host = value
                    elif key == 'DB_USER':
                        db_user = value
                    elif key == 'DB_PASSWORD':
                        db_password = value
                    elif key == 'DB_NAME':
                        db_name = value
        except FileNotFoundError:
            print("Error: Database key file not found.")
        except Exception as e:
            print(f"Error reading database key file: {e}")

        return db_host, db_user, db_password, db_name
    def check_and_fix_date(self,date_str):
        try:
            # Attempt to parse the date string with the expected format
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str  # Return the original date string if it's in the correct format
        except ValueError:
            try:
                # Try to parse the date string with a different format
                parsed_date = datetime.strptime(date_str, "%m/%d/%Y")
                return parsed_date.strftime("%Y-%m-%d")  # Return the fixed date string in the correct format
            except ValueError:
                # If both attempts fail, return None or raise an exception, depending on your requirements
                return None
    def sub_category(self):
        db_host, db_user, db_password, db_name = self.db_connecter()
        return_list = self.get_category.Get_Sub_Category(db_host, db_user, db_password, db_name)
        return return_list
    
    def update_table(self,lookup_month_name, year):
        db_host, db_user, db_password, db_name = self.db_connecter()
        return_list = self.view_budget.view_Budget(db_host,db_user, db_password, db_name, lookup_month_name, year)
        return return_list

    def add_transaction(self,date, note, amount, category, sub_category):
        db_host, db_user, db_password, db_name = self.db_connecter()
        new_date = self.check_and_fix_date(date)
        if category == "Income":
            self.add_income.Add_income(db_host, db_user, db_password, db_name, new_date, note, amount, sub_category)
        elif category == "Expense":
            self.add_expense.Add_expense(db_host, db_user, db_password, db_name, new_date, note, amount, sub_category) 
        elif category == "Fixed Expense":
            self.add_fixed_expense.Add_Fixed_expense(db_host, db_user, db_password, db_name, date, note, amount, sub_category)
        else:
            return ("fail")
    def Create_transfer(self,From_account, To_account, Transfer_date, note, amount):
        db_host, db_user, db_password, db_name = self.db_connecter()
        
        if To_account == "Checking":
            To_account = 'Checking_Account'
        elif To_account == "Bail out":
            To_account = 'Bail_Out'
        elif To_account == "saving":
            To_account = 'Savings'
            
        if From_account == "Checking":
            From_account = 'Checking_Account'
        elif From_account == "Bail out":
            From_account = 'Bail_Out'
        elif From_account == "saving":
            From_account = 'Savings'
        
        
        self.Transfer.Create_Transfer(db_host, db_user, db_password, db_name, From_account, To_account, Transfer_date, note, amount)
            
    def look_up_expense(self,look_up_date):
        db_host, db_user, db_password, db_name = self.db_connecter()
        return_list = self.find_expense_by_date.view_expense(db_host, db_user, db_password, db_name, look_up_date)
        return return_list
        
        
#source venv/bin/activate




