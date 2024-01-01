from Refresh_db.update_checking import update_checking_account
from Refresh_db.update_saveings import Update_saveings_account
from Refresh_db.update_bailout import Update_bailout_account
checking_account_update = update_checking_account()
saveing_account_update = Update_saveings_account()
bailout_account_update = Update_bailout_account()


class update_all_accounts:
    @classmethod
    def Update_all_accounts(cls,db_host, db_user,db_password,db_name,table_name,year):
        checking_account_update.Update_Checking_account(db_host, db_user,db_password,db_name,table_name,year)
        saveing_account_update.Update_Saveing_account(db_host, db_user,db_password,db_name,table_name,year)
        bailout_account_update.Update_bailout_account(db_host, db_user,db_password,db_name,table_name,year)