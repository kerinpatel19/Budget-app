import tkinter as tk
from datetime import datetime, timedelta
from controller import Controller 


class BudgetApp:
    def __init__(self, root):
        self.Controller = Controller()
        self.root = root
        #self.root.geometry('800x400')
        self.root.title("Budget App")
        self.root.config(background="#ffffff")

        self.create_all_frames()
        self.create_control_buttons_frame()
        self.default_input_area_screen()

        # Adjust the app size to fit the content
        self.root.update_idletasks()
        self.root.geometry(f"{self.root.winfo_reqwidth()}x{self.root.winfo_reqheight()}")
        self.current_month_displayed = "none"
        
        
    def create_all_frames(self):
        
        self.budget_table_frame = tk.LabelFrame(self.root, text="Budget Table")
        self.budget_table_frame.grid(row=0, column=0, sticky="w",)
        self.current_month_budget_table_frame()
    
    def clear_budget_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.budget_table_frame.winfo_children():
            widget.destroy() 
    
    def current_month_budget_table_frame(self):
        self.clear_budget_screen()
        
        todays_month = datetime.now().strftime("%B")
        #todays_year = int(datetime.now().strftime("%Y"))
        todays_year = 2023
        return_list = self.Controller.update_table(todays_month,todays_year)
        
        labels = ["Date", "Main Account", "Saving Account", "Bail-Out Account"]
        for col, label in enumerate(labels):
            tk.Label(self.budget_table_frame, text=label).grid(row=2, column=col)

        data = return_list

        for row, entry_data in enumerate(data, start=3):
            for col, value in enumerate(entry_data):
                entry = tk.Label(self.budget_table_frame, text=value, width=10, justify='center')
                entry.grid(row=row, column=col)
        self.current_month_displayed = todays_month
        
                
    def last_month_budget_table_frame(self):
        
        self.clear_budget_screen()

        previous_month = (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1).strftime("%B")
        previous_month_year = 2023
        
        #previous_month = datetime.strftime("%B")
        return_list = self.Controller.update_table(previous_month,previous_month_year)
        
        self.budget_table_frame = tk.LabelFrame(self.root, text="Budget Table")
        self.budget_table_frame.grid(row=0, column=0, sticky="w",)
        labels = ["Date", "Main Account", "Saving Account", "Bail-Out Account"]
        for col, label in enumerate(labels):
            tk.Label(self.budget_table_frame, text=label).grid(row=2, column=col)

        data = return_list

        for row, entry_data in enumerate(data, start=3):
            for col, value in enumerate(entry_data):
                entry = tk.Label(self.budget_table_frame, text=value, width=10, justify='center')
                entry.grid(row=row, column=col)
        self.current_month_displayed = previous_month
        
    def next_month_budget_table_frame(self):
        # Clear existing content of budget_table_frame by updating label texts
        for label in self.budget_table_frame.grid_slaves():
            label.config(text="")

        # Convert the current month string to a datetime object
        current_month_date = datetime.strptime(self.current_month_displayed, "%b")

        # Add one month to the datetime object
        next_month_date = current_month_date + timedelta(month=1)

        # Convert the resulting datetime object back to a string
        next_month_str = next_month_date.strftime("%b")
        self.current_month_displayed = next_month_str
        next_month_year = 2023

        return_list = self.Controller.update_table(next_month_str, next_month_year)
        print("Debug: Return list:", return_list)
        labels = ["Date", "Main Account", "Saving Account", "Bail-Out Account"]
        for col, label_text in enumerate(labels):
            tk.Label(self.budget_table_frame, text=label_text).grid(row=2, column=col)

        if return_list:
            for row, entry_data in enumerate(return_list, start=3):
                for col, value in enumerate(entry_data):
                    entry = tk.Label(self.budget_table_frame, text=value, width=10, justify='center')
                    entry.grid(row=row, column=col)

        self.current_month_displayed = next_month_str

    def create_control_buttons_frame(self):
        self.frame2 = tk.Frame(self.root)
        self.frame2.grid(row=0, column=1, rowspan=4, columnspan= 2, sticky="nsew")
        
        self.control_frame = tk.LabelFrame(self.frame2, text="Budget Controls")
        self.control_frame.grid(row=1, column=0)

        tk.Button(self.control_frame, text="Transfer", width=5, height=4, command= self.create_transfer_screen).grid(row=0, column=0, columnspan=1, rowspan=1, sticky="ew")
        tk.Button(self.control_frame, text="Add Income", width=5, height=4, command= self.create_income_screen).grid(row=0, column=1, columnspan=1, rowspan=1, sticky="ew")
        tk.Button(self.control_frame, text="Expense", width=5, height=4, command=self.create_expense_screen).grid(row=0, column=2, columnspan=1, rowspan=1, sticky="ew")
        tk.Button(self.control_frame, text="Edit Expense", width=5, height=4, command=self.create_Edit_expense_screen).grid(row=0, column=3, columnspan=1, rowspan=1, sticky="ew")
        
        tk.Button(self.control_frame, text="last month", height=2, command=self.last_month_budget_table_frame).grid(row=2, column=0, columnspan=1, rowspan=1, sticky="n")
        tk.Button(self.control_frame, text="Current month", height=2, command=self.current_month_budget_table_frame).grid(row=2, column=1, columnspan=2, rowspan=2, sticky="ew")
        tk.Button(self.control_frame, text="Next month", height=2, command=self.next_month_budget_table_frame).grid(row=2,column=3, columnspan=1, rowspan=1, sticky="n")
        
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

    

    
    
        
if __name__ == "__main__":
    window = tk.Tk()
    app = BudgetApp(window)
    window.mainloop()
    
#source venv/bin/activate
