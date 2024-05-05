from controller import Controller
import mysql.connector
from Output_data.yearly_summary import Get_summary
controller = Controller()
summary = Get_summary()

db_host, db_user, db_password, db_name = controller.db_connecter()
year = 2024
list_return = summary.get_month_data(db_host, db_user, db_password, db_name, year)

print(list_return)