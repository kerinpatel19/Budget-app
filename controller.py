from datetime import datetime, timedelta
from Output_data import view_monthly_budget


class Controller:
    
    def __init__(self):
        self.view_budget = view_monthly_budget.view_budget()  # Instantiate the view_budget class

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
        print(print("step 2 done"))

        return db_host, db_user, db_password, db_name

    
    def update_table(self,lookup_month_name, year):
        db_host, db_user, db_password, db_name = self.db_connecter()
        return_list = self.view_budget.view_Budget(db_host,db_user, db_password, db_name, lookup_month_name, year)
        print("step 3 done")
        return return_list


#source venv/bin/activate




