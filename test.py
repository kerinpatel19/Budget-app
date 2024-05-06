from controller import Controller
import mysql.connector
from Output_data.yearly_summary import Get_summary
controller = Controller()
summary = Get_summary()

db_host, db_user, db_password, db_name = controller.db_connecter()
start_Date = ""
list_return = controller.update_year_summary(start_Date)

print(list_return)