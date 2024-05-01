from datetime import datetime, timedelta
from Output_data import view_monthly_budget
from Output_data import view_expense_by_sub_category
from Output_data.get_category_by_control_category import GetCategory
from Output_data import view_expense_by_dates
from Output_data.view_table_names import View_table_names
from Input_data.Add_starting_balance import StartBalance
from Input_data.Add_income import Add_Income
from Input_data.Add_expense import Add_Expense
from Input_data.Create_transfer import Transfer_money
from Input_data.Add_fixed_expense import Add_fixed_expense
from Data_base.Create_database import Create_data_base
from Data_base.Create_new_table import Create_table
from Data_base.Delete_year import delete_year
from Input_data.Add_starting_balance import StartBalance
from data_extract.data_sorter import line_extract
from Ledger import update_expense
from Refresh_db.update_checking import update_checking_account
from Remove_data.Delete_expense import Delete_expense
class Controller:
    
    def __init__(self):
        self.view_budget = view_monthly_budget.view_budget()  # Instantiate the view_budget class
        self.find_expense_by_subcategories = view_expense_by_sub_category.view_Expense()
        self.find_expense_by_date = view_expense_by_dates.view_Expense_date()
        self.view_table = View_table_names()
        self.add_starting_bal= StartBalance()
        self.add_income = Add_Income()
        self.add_expense = Add_Expense()
        self.Transfer = Transfer_money()
        self.add_fixed_expense = Add_fixed_expense()
        self.get_category = GetCategory()
        self.database_creator = Create_data_base()
        self.table_creator = Create_table()
        self.Delete_year = delete_year()
        self.Starter_balance = StartBalance()
        self.sort_data = line_extract()
        self.update_expense = update_expense.update_expense()
        self.checking_account_update = update_checking_account()
        self.delete_expense = Delete_expense ()
        
    def db_connecter(self):
        db_host = None
        db_user = None
        db_password = None
        db_name = None
        file_path = "/Users/kerinpatel/Desktop/Projects-python/Budget_app/config.gitingore/database_key.txt"
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

    def sub_category(self,Control_Category):
        return_list = []
        db_host, db_user, db_password, db_name = self.db_connecter()
        if Control_Category != "all":
            return_list = self.get_category.get_category(db_host, db_user, db_password, db_name,Control_Category)
        else:
            Control_Category_list = ["Transfer","Income","Expense"]
            for Control_category in range(len(Control_Category_list)):
                List = self.get_category.get_category(db_host, db_user, db_password, db_name,Control_category)
                for i in range(len(List)):
                    return_list.append(List[i])
        return return_list
        

    def update_table(self,lookup_month_name, year):
        db_host, db_user, db_password, db_name = self.db_connecter()
        return_list = self.view_budget.view_Budget(db_host,db_user, db_password, db_name, lookup_month_name, year)
        return return_list
    
    def add_starting_balance(self, year, checking_account, bail_out, savings,Bank_verified):
        db_host, db_user, db_password, db_name = self.db_connecter()
        message = self.add_starting_bal.add_starting_balance(db_host, db_user, db_password, db_name, year, checking_account, bail_out, savings,Bank_verified)
        return message

    def add_transaction(self,date, note, amount, category, sub_category,Bank_verified):
        db_host, db_user, db_password, db_name = self.db_connecter()
        new_date = self.check_and_fix_date(date)
        if category == "Income":
            self.add_income.Add_income(db_host, db_user, db_password, db_name, new_date, note, amount, sub_category,Bank_verified)
        elif category == "Expense":
            self.add_expense.Add_expense(db_host, db_user, db_password, db_name, new_date, note, amount, sub_category,Bank_verified) 
        elif category == "Fixed Expense":
            self.add_fixed_expense.Add_Fixed_expense(db_host, db_user, db_password, db_name, date, note, amount, sub_category,Bank_verified)
        elif category == "Expense-Unsorted":
            self.add_expense.Add_expense(db_host, db_user, db_password, db_name, new_date, note, amount, sub_category,Bank_verified) 
        elif category == "Income-Unsorted":
            self.add_income.Add_income(db_host, db_user, db_password, db_name, new_date, note, amount, sub_category,Bank_verified)
        
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
            
    def look_up_expense(self,look_up_date, sub_catogeiors):
        db_host, db_user, db_password, db_name = self.db_connecter()
        return_list = self.find_expense_by_subcategories.view_expense(db_host, db_user, db_password, db_name, look_up_date, sub_catogeiors)
        return return_list

    def look_up_expense_by_date(self,look_up_date):
        db_host, db_user, db_password, db_name = self.db_connecter()
        return_list = self.find_expense_by_date.view_expense_by_date(db_host, db_user, db_password, db_name, look_up_date)
        return return_list        
    
    def add_year(self,table_name,year):
        db_host, db_user, db_password, db_name = self.db_connecter()
        num = self.table_creator.populate_single_table( db_host, db_user, db_password, db_name, table_name,year)
        if num == True:
            return f"{year} - successfully added"
        else:
            return f"Failed to add year - {year}"
    
    def delete_year(self,year):
        db_host, db_user, db_password, db_name = self.db_connecter()
        num = self.Delete_year.delete_year_table(db_host, db_user, db_password, db_name,year)
        if num == True:
            return f"{year} - successfully Deleted"
        else:
            return f"Failed to Delete year - {year}"
    
    def delete_expense_row(self, row_ID, row_date,year):
        db_host, db_user, db_password, db_name = self.db_connecter()
        self.delete_expense.delete_expense(db_host, db_user, db_password, db_name, row_ID, row_date,year)
        
        
    def View_all_year_table(self):
        db_host, db_user, db_password, db_name = self.db_connecter()
        return_list = self.view_table.View_all_table(db_host, db_user, db_password, db_name)
        return return_list
    
    def List_injector(self, List):
        
        for i in range(len(List)):
            #if date == "****-12-31":
                
            date = List[i][0]
            note = List[i][1]
            amount = List[i][2]
            category = List[i][3]
            sub_category = List[i][4]
            self.add_transaction(date, note, amount, category, sub_category,True)
        
        date = datetime.strptime(List[-1][0], "%Y-%m-%d")
        table_name = f"Budget{date.year}"
        db_host, db_user, db_password, db_name = self.db_connecter()
        self.checking_account_update.Update_Checking_account(db_host, db_user,db_password,db_name,table_name,date.year)

                
    def Update_expense(self,transaction_date,account,note,amount,new_category):
        db_host, db_user, db_password, db_name = self.db_connecter()
        self.update_expense.update(db_host, db_user, db_password, db_name,transaction_date,account,note,amount,new_category)
    
    def Process_pdf(self, path_name):
        db_host, db_user, db_password, db_name = self.db_connecter()
        return_list = self.sort_data.extract_lines(path_name,db_host, db_user, db_password, db_name)
        self.List_injector(return_list)
        

    
        

#source venv/bin/activate




