import tkinter as tk
from datetime import datetime, timedelta
from controller import Controller 


class BudgetApp:
    def __init__(self, root):
        self.Controller = Controller()
        self.root = root
        self.root.geometry('800x400')
        self.root.title("Budget App")
        self.root.config(background="#ffffff")

        self.create_budget_table_frame()
        self.create_control_buttons_frame()
        self.create_input_screen_buttons_frame()

    def create_budget_table_frame(self):
        print("step 1 done")
        todays_month = datetime.now().strftime("%B")
        #todays_year = int(datetime.now().strftime("%Y"))
        todays_year = 2023
        return_list = self.Controller.update_table(todays_month,todays_year)
        
        budget_table_frame = tk.LabelFrame(self.root, text="Budget Table")
        budget_table_frame.grid(row=0, column=0, sticky="w")
        print("step 5 done")
        labels = ["Date", "Main Account", "Saving Account", "Bail-Out Account"]
        for col, label in enumerate(labels):
            tk.Label(budget_table_frame, text=label).grid(row=2, column=col)

        data = return_list

        for row, entry_data in enumerate(data, start=3):
            for col, value in enumerate(entry_data):
                entry = tk.Label(budget_table_frame, text=value, width=10, justify='center')
                entry.grid(row=row, column=col)

    def create_control_buttons_frame(self):
        frame2 = tk.Frame(self.root)
        frame2.grid(row=0, column=1, rowspan=4, columnspan= 2, sticky="n")
        
        control_frame = tk.LabelFrame(frame2, text="Budget Controls")
        control_frame.grid(row=1, column=0)

        tk.Button(control_frame, text="Transfer", width=5, height=4).grid(row=0, column=0)
        tk.Button(control_frame, text="Add Income", width=5, height=4).grid(row=0, column=1)
        tk.Button(control_frame, text="Expense", width=5, height=4).grid(row=0, column=2)
        tk.Button(control_frame, text="Edit Expense", width=5, height=4).grid(row=0, column=3)
        tk.Label(control_frame, text="Text", width=20, height=10).grid(row=1, column=0, rowspan=4, sticky="n")

    def create_input_screen_buttons_frame(self):
        frame3 = tk.Frame(self.root)
        frame3.grid(row=0, column=1)
        #sticky="e"
        #tk.Label(frame3, text="Text", width=20, height=10).grid(row=4, column=0, sticky="n")

if __name__ == "__main__":
    window = tk.Tk()
    app = BudgetApp(window)
    window.mainloop()
    
#source venv/bin/activate
