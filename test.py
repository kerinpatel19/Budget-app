from Output_data.view_tabel_names import View_table_names
from controller import Controller

controller = Controller()
view_table = View_table_names()

db_host, db_user, db_password, db_name = controller.db_connecter()

name_list = view_table.View_all_table(db_host, db_user, db_password, db_name)

print(name_list)
        