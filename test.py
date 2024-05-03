#from controller import Controller
#
#controller = Controller()
#
#db_host, db_user, db_password, db_name = controller.db_connecter()
#start_date = "2024-04-06"
#data = "Transfer"
#name_list = controller.look_up_expense(start_date, data)
#
#print(name_list)
from datetime import datetime, timedelta

# Starting date of the month
start_date = datetime(2024, 7, 1)

# Calculate the end of the month
if start_date.month == 12:
    end_date = start_date.replace(day=1, month=1, year=start_date.year + 1)
else:
    end_date = start_date.replace(day=1, month=start_date.month + 1)

end_date -= timedelta(days=1)

print("End of the month date:", end_date.date())
