import customtkinter as ctk
from datetime import datetime
from dateutil.relativedelta import relativedelta
from controller import Controller


class Budget_frame_L(ctk.CTkFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.Controller = Controller()
        self.current = datetime.now()
        self.current_month_budget_table_frame()
    
    def clear_budget_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.winfo_children():
            widget.destroy()
        
    
    def current_month_budget_table_frame(self):
        self.clear_budget_screen()
        self.current_month_displayed = self.current
        todays_year = self.current_month_displayed.year
        todays_month= self.current.strftime("%B")
        return_list = self.Controller.update_table(todays_month,todays_year)
        
        labels = ["        Date         ", "Main Account", "Bail-Out Account","Saving Account", 
                "transfer out", "transfer In",
                "income", "expense"]
        for col, label in enumerate(labels):
            ctk.CTkLabel(self, text=label).grid(row=2, column=col)

        data = return_list

        for row, entry_data in enumerate(data, start=3):
            for col, value in enumerate(entry_data):
                entry = ctk.CTkLabel(self, text=value, width=10, justify='center')
                entry.grid(row=row, column=col)
        self.control_frame_R.monthly_overview(return_list)
        
    def last_month_budget_table_frame(self):
        
        self.clear_budget_screen()

        previous_month = self.current_month_displayed - relativedelta(months=1)
        self.current_month_displayed = previous_month
        year = self.current_month_displayed.year
        month= self.current_month_displayed.strftime("%B")
        return_list = self.Controller.update_table(month,year)
        labels = ["        Date         ", "Main Account", "Bail-Out Account","Saving Account", 
                "transfer out", "transfer In",
                "income", "expense"]
        for col, label in enumerate(labels):
            ctk.CTkLabel(self, text=label, borderwidth=2).grid(row=2, column=col)

        data = return_list

        for row, entry_data in enumerate(data, start=3):
            for col, value in enumerate(entry_data):
                entry = ctk.CTkLabel(self, text=value, width=10, justify='center')
                entry.grid(row=row, column=col)
        self.control_frame_R.monthly_overview(return_list)
        
    def next_month_budget_table_frame(self):
        self.clear_budget_screen()

        next_month = self.current_month_displayed + relativedelta(months=1)
        self.current_month_displayed = next_month
        year = self.current_month_displayed.year
        month= self.current_month_displayed.strftime("%B")
        return_list = self.Controller.update_table(month,year)
        labels = ["        Date         ", "Main Account", "Bail-Out Account","Saving Account", 
                "transfer out", "transfer In",
                "income", "expense"]
        for col, label in enumerate(labels):
            ctk.CTkLabel(self, text=label, borderwidth=2).grid(row=2, column=col)

        data = return_list
        
        for row, entry_data in enumerate(data, start=3):
            for col, value in enumerate(entry_data):
                entry = ctk.CTkLabel(self, text=value, width=10, justify='center')
                entry.grid(row=row, column=col)
        self.control_frame_R.monthly_overview(return_list)
        
    def custom_month_budget_table_frame(self, date):
        from control_frame_R import Control_frame_R
        control_frame_R = Control_frame_R()
        self.clear_budget_screen()
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        self.current_month_displayed = date_obj
        custom_year = self.current_month_displayed.year
        custom_month= self.current_month_displayed.strftime("%B")
        return_list = self.Controller.update_table(custom_month,custom_year)
        
        labels = ["        Date         ", "Main Account", "Bail-Out Account","Saving Account", 
                "transfer out", "transfer In",
                "income", "expense"]
        for col, label in enumerate(labels):
            ctk.CTkLabel(self, text=label, corner_radius=2).grid(row=2, column=col)

        data = return_list

        for row, entry_data in enumerate(data, start=3):
            for col, value in enumerate(entry_data):
                entry = ctk.CTkLabel(self, text=value, width=10, justify='center')
                entry.grid(row=row, column=col)
        control_frame_R.monthly_overview(return_list)