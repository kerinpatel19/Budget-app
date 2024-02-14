import tkinter as tk
from datetime import datetime, timedelta
from controller import Controller 
from dateutil.relativedelta import relativedelta


class BudgetApp:
    def __init__(self, root):
        self.Controller = Controller()
        self.root = root
        #self.root.geometry('800x400')
        self.root.title("Budget App")
        self.root.config(background="#ffffff")
        self.current = datetime.now()

        self.create_all_frames()
        self.create_control_buttons_frame()
        self.default_input_area_screen()

        # Adjust the app size to fit the content
        self.root.update_idletasks()
        self.root.geometry(f"{self.root.winfo_reqwidth()}x{self.root.winfo_reqheight()}")
        
        self.current_month_displayed = self.current
        
    def create_all_frames(self):
        
        self.budget_table_frame = tk.LabelFrame(self.root, text="Budget Table")
        self.budget_table_frame.grid(row=0, column=0, sticky="w",)
        
        self.frame2 = tk.Frame(self.root)
        self.frame2.grid(row=0, column=1, rowspan=4, columnspan= 2, sticky="nsew")
        
        self.control_frame = tk.LabelFrame(self.frame2, text="Budget Controls")
        self.control_frame.grid(row=1, column=0)
        self.current_month_budget_table_frame()
        
    
    def clear_budget_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.budget_table_frame.winfo_children():
            widget.destroy()
        
    
    def current_month_budget_table_frame(self):
        self.clear_budget_screen()
        self.current_month_displayed = self.current
        todays_year = self.current_month_displayed.year
        todays_month= self.current.strftime("%B")
        return_list = self.Controller.update_table(todays_month,todays_year)
        
        labels = ["        Date         ", "Main Account", "Saving Account", "Bail-Out Account"]
        for col, label in enumerate(labels):
            tk.Label(self.budget_table_frame, text=label, relief=tk.SOLID, borderwidth=2).grid(row=2, column=col)

        data = return_list

        for row, entry_data in enumerate(data, start=3):
            for col, value in enumerate(entry_data):
                entry = tk.Label(self.budget_table_frame, text=value, width=10, justify='center', relief=tk.SOLID, borderwidth=2)
                entry.grid(row=row, column=col)      
    def last_month_budget_table_frame(self):
        
        self.clear_budget_screen()

        previous_month = self.current_month_displayed - relativedelta(months=1)
        self.current_month_displayed = previous_month
        year = self.current_month_displayed.year
        month= self.current_month_displayed.strftime("%B")
        return_list = self.Controller.update_table(month,year)
        labels = ["        Date         ", "Main Account", "Saving Account", "Bail-Out Account"]
        for col, label in enumerate(labels):
            tk.Label(self.budget_table_frame, text=label, relief=tk.SOLID, borderwidth=2).grid(row=2, column=col)

        data = return_list

        for row, entry_data in enumerate(data, start=3):
            for col, value in enumerate(entry_data):
                entry = tk.Label(self.budget_table_frame, text=value, width=10, justify='center', relief=tk.SOLID, borderwidth=2)
                entry.grid(row=row, column=col)
    def next_month_budget_table_frame(self):
        self.clear_budget_screen()

        next_month = self.current_month_displayed + relativedelta(months=1)
        self.current_month_displayed = next_month
        year = self.current_month_displayed.year
        month= self.current_month_displayed.strftime("%B")
        return_list = self.Controller.update_table(month,year)
        labels = ["        Date         ", "Main Account", "Saving Account", "Bail-Out Account"]
        for col, label in enumerate(labels):
            tk.Label(self.budget_table_frame, text=label, relief=tk.SOLID, borderwidth=2).grid(row=2, column=col)

        data = return_list

        for row, entry_data in enumerate(data, start=3):
            for col, value in enumerate(entry_data):
                entry = tk.Label(self.budget_table_frame, text=value, width=10, justify='center', relief=tk.SOLID, borderwidth=2)
                entry.grid(row=row, column=col)
    def create_control_buttons_frame(self):

        tk.Button(self.control_frame, text="Transfer", width=5, height=4, command= self.create_transfer_screen).grid(row=0, column=0, columnspan=1, rowspan=1, sticky="ew")
        tk.Button(self.control_frame, text="Add Income", width=5, height=4, command= self.create_income_screen).grid(row=0, column=1, columnspan=1, rowspan=1, sticky="ew")
        tk.Button(self.control_frame, text="Expense", width=5, height=4, command=self.create_expense_screen).grid(row=0, column=2, columnspan=1, rowspan=1, sticky="ew")
        tk.Button(self.control_frame, text="Edit Expense", width=5, height=4, command=self.create_Edit_expense_screen).grid(row=0, column=3, columnspan=1, rowspan=1, sticky="ew")
        
        tk.Button(self.control_frame, text="last month", height=2, command=self.last_month_budget_table_frame).grid(row=2, column=0, columnspan=1, rowspan=1, sticky="n")
        tk.Button(self.control_frame, text="Current month", height=2, command=self.current_month_budget_table_frame).grid(row=2, column=1, columnspan=2, rowspan=2, sticky="ew")
        tk.Button(self.control_frame, text="Next month", height=2, command=self.next_month_budget_table_frame).grid(row=2,column=3, columnspan=1, rowspan=1, sticky="n")
        

   #row 2   frame 2  
    def default_input_area_screen(self):
        self.control_frame_view = tk.LabelFrame(self.frame2, text="Input area")
        self.control_frame_view.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)  # Align to bottom with padding
        tk.Label(self.control_frame_view, text="Text", width=20, height=10).grid(row=1, column=0, rowspan=4, sticky="n")
    def create_transfer_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()
        self.control_frame_view.config(text="Transfer Form" , bg="#8e9bb9")

        # Create transfer input form
        tk.Label(self.control_frame_view, text="Transfer entry data here", width=20, height=10).grid(row=0, column=0)
        # Add relevant input fields and buttons for transfer screen
    def create_income_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()
        self.control_frame_view.config(text="Income Form", bg="#9cbce4")

        # Create transfer input form
        tk.Label(self.control_frame_view, text="Income entry data here" , width=20, height=10).grid(row=0, column=0)
        # Add relevant input fields and buttons for transfer screen
    def create_expense_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()
        self.control_frame_view.config(text="expense Form", bg="#d5d5e1")

        # Create transfer input form
        tk.Label(self.control_frame_view, text="expense entry data here" , width=20, height=10).grid(row=0, column=0)
        # Add relevant input fields and buttons for transfer screen
    def create_Edit_expense_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()
        self.control_frame_view.config(text="Edit expense Form", bg="#4475b8")

        # Create transfer input form
        tk.Label(self.control_frame_view, text="which one" , width=20, height=10).grid(row=0, column=0)
        # Add relevant input fields and buttons for transfer screen

    #row 3 frame 2
    
    def monthly_overview(self):
        year = self.current_month_displayed.year
        month= self.current_month_displayed.strftime("%B")
        try:
            return_list = self.Controller.update_table(month,year)
        
        except:
            return_list = ["Na"]

        i = 0
        for i in return_list[i]:
            if i == 0:
                print(0)
                

        
        
        self.control_frame_view = tk.LabelFrame(self.frame2, text="Input area")
        self.control_frame_view.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)  # Align to bottom with padding
        tk.Label(self.control_frame_view, text="Text", width=20, height=10).grid(row=1, column=0, rowspan=4, sticky="n")
        
if __name__ == "__main__":
    window = tk.Tk()
    app = BudgetApp(window)
    window.mainloop()
    
#source venv/bin/activate