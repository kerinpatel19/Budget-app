import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from controller import Controller
from dateutil.relativedelta import relativedelta
import calendar

class BudgetApp:
    def __init__(self, root):
        self.Controller = Controller()
        self.root = root
        #self.root.geometry('800x400')
        self.root.title("Budget App")
        self.root.config(background="#ffffff")
        self.current = datetime.now()
        self.accounts = ["Checking", "Bail out", "saving"]
        self.style = ttk.Style()
        self.style.configure('Custom.TFrame', background='#FF0000')



        self.create_all_frames()
        self.create_control_buttons_frame()
        self.default_input_area_screen()
        self.current_month_budget_table_frame()

        # Adjust the app size to fit the content
        self.root.update_idletasks()
        self.root.geometry(f"{self.root.winfo_reqwidth()}x{self.root.winfo_reqheight()}")
        
        self.current_month_displayed = self.current
        
    def create_all_frames(self):
        
        self.budget_table_frame = ttk.LabelFrame(self.root, text="Budget Table", style='Custom.TFrame')
        self.budget_table_frame.grid(row=0, column=0, sticky="w",)
        
        self.frame2_control = ttk.Frame(self.root, style='Custom.TFrame')
        self.frame2_control.grid(row=0, column=1, rowspan=4, columnspan= 2, sticky="nsew")
        
        self.control_frame = ttk.LabelFrame(self.frame2_control, text="Budget Controls", style='Custom.TFrame')
        self.control_frame.grid(row=1, column=0)
        
        
        self.control_frame_view = ttk.LabelFrame(self.frame2_control, text="Input area", style='Custom.TFrame')
        self.control_frame_view.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        
    
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
        
        labels = ["        Date         ", "Main Account", "Bail-Out Account","Saving Account", 
                "transfer out", "transfer In",
                "income", "expense"]
        for col, label in enumerate(labels):
            ttk.Label(self.budget_table_frame, text=label, relief=tk.SOLID, borderwidth=2).grid(row=2, column=col)

        data = return_list

        for row, entry_data in enumerate(data, start=3):
            for col, value in enumerate(entry_data):
                entry = ttk.Label(self.budget_table_frame, text=value, width=10, justify='center', relief='solid', borderwidth=2)
                entry.grid(row=row, column=col)   
        self.monthly_overview(return_list)
        
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
            ttk.Label(self.budget_table_frame, text=label, relief=tk.SOLID, borderwidth=2).grid(row=2, column=col)

        data = return_list
        self.monthly_overview(return_list)

        for row, entry_data in enumerate(data, start=3):
            for col, value in enumerate(entry_data):
                entry = ttk.Label(self.budget_table_frame, text=value, width=10, justify='center', relief='solid', borderwidth=2)
                entry.grid(row=row, column=col)
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
            ttk.Label(self.budget_table_frame, text=label, relief=tk.SOLID, borderwidth=2).grid(row=2, column=col)

        data = return_list
        self.monthly_overview(return_list)
        
        for row, entry_data in enumerate(data, start=3):
            for col, value in enumerate(entry_data):
                entry = ttk.Label(self.budget_table_frame, text=value, width=10, justify='center', relief=tk.SOLID, borderwidth=2)
                entry.grid(row=row, column=col)
                
    def custom_month_budget_table_frame(self, date):
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
            ttk.Label(self.budget_table_frame, text=label, relief=tk.SOLID, borderwidth=2).grid(row=2, column=col)

        data = return_list

        for row, entry_data in enumerate(data, start=3):
            for col, value in enumerate(entry_data):
                entry = ttk.Label(self.budget_table_frame, text=value, width=10, justify='center', relief=tk.SOLID, borderwidth=2)
                entry.grid(row=row, column=col)   
        self.monthly_overview(return_list)
    def create_control_buttons_frame(self):

        ttk.Button(self.control_frame, text="Transfer", width=5, padding=4, command= self.create_transfer_screen).grid(row=0, column=0, columnspan=1, rowspan=1, sticky="ew")
        ttk.Button(self.control_frame, text="Add Income", width=5, padding=4, command= self.create_income_screen).grid(row=0, column=1, columnspan=1, rowspan=1, sticky="ew")
        ttk.Button(self.control_frame, text="Expense", width=5, padding=4, command=self.create_expense_screen).grid(row=0, column=2, columnspan=1, rowspan=1, sticky="ew")
        ttk.Button(self.control_frame, text="Edit Expense", width=5, padding=4, command=self.create_Edit_expense_screen).grid(row=0, column=3, columnspan=1, rowspan=1, sticky="ew")
        
        ttk.Button(self.control_frame, text="last month", padding=4, command=self.last_month_budget_table_frame).grid(row=2, column=0, columnspan=1, rowspan=1, sticky="wen")
        ttk.Button(self.control_frame, text="Current month", padding=4, command=self.current_month_budget_table_frame).grid(row=2, column=1, columnspan=2, rowspan=1, sticky="ew")
        ttk.Button(self.control_frame, text="Next month", padding=4, command=self.next_month_budget_table_frame).grid(row=2,column=3, columnspan=1, rowspan=1, sticky="wen")
  
        ttk.Button(self.control_frame, text="scan statement", padding=4, command=self.last_month_budget_table_frame).grid(row=3, column=0, columnspan=1, rowspan=1, sticky="ewn")
        ttk.Button(self.control_frame, text="Add more year", padding=4, command=self.current_month_budget_table_frame).grid(row=3, column=1, columnspan=1, rowspan=1, sticky="ew")
        ttk.Button(self.control_frame, text="Add Category", padding=4, command=self.next_month_budget_table_frame).grid(row=3,column=2, columnspan=1, rowspan=1, sticky="ewn")
        ttk.Button(self.control_frame, text="More", padding=4, command=self.next_month_budget_table_frame).grid(row=3,column=3, columnspan=1, rowspan=1, sticky="ewn")
  
    def get_sub_category_list(self):
        return_list = self.Controller.sub_category()
        return return_list
    #row 2   frame 2  
    def default_input_area_screen(self):  # Align to bottom with padding
        ttk.Label(self.control_frame_view, text="Text", width=20, padding=10, background="lightblue").grid(row=1, column=0, rowspan=4, sticky="n")
    def create_transfer_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()

            # Create a new style for the LabelFrame
        style = ttk.Style()
        style.configure("Custom.TLabelframe", background='#FF0000')

        # Configure the LabelFrame with the custom style
        self.control_frame_view.config(text="Transfer Form", style=style)

        def reset_list():
            self.accounts.clear()
            self.accounts = ["Checking", "Bail out", "saving"]
            combo_a['values'] = self.accounts
            combo_b['values'] = self.accounts
        
        def update_to_options(event):
            combo_box_a = combo_a.get()
            combo_box_b = combo_b.get()
            if combo_box_a is not None:
                self.accounts.remove(combo_box_a)
                combo_b.set("")  # Clear the current selection
                combo_b['values'] = self.accounts
            else:
                self.accounts.remove(combo_box_b)
                combo_a.set("")  # Clear the current selection
                combo_a['values'] = self.accounts

        ttk.Label(self.control_frame_view, text="From Account:").grid(row=0, column=0)
        combo_a = ttk.Combobox(self.control_frame_view, values=self.accounts)
        combo_a.grid(row=0, column=1)
        combo_a.bind("<<ComboboxSelected>>", update_to_options)


        ttk.Label(self.control_frame_view, text="To Account:").grid(row=1, column=0)
        combo_b = ttk.Combobox(self.control_frame_view, values=self.accounts)
        combo_b.grid(row=1, column=1)
        combo_b.bind("<<ComboboxSelected>>", update_to_options)



        ttk.Label(self.control_frame_view, text="Date: ").grid(row=2, column=0)
        transfer_date_entry = ttk.Entry(self.control_frame_view)
        transfer_date_entry.insert(0, "YYYY-MM-DD")  # Set initial text
        transfer_date_entry.bind("<FocusIn>", lambda event: transfer_date_entry.delete(0, "end"))  # Remove text on focus
        transfer_date_entry.grid(row=2, column=1)

        ttk.Label(self.control_frame_view, text="Note:").grid(row=3, column=0)
        note_entry = ttk.Entry(self.control_frame_view)
        note_entry.insert(0, "ABC...")  # Set initial text
        note_entry.bind("<FocusIn>", lambda event: note_entry.delete(0, "end"))  # Remove text on key release
        note_entry.grid(row=3, column=1)

        ttk.Label(self.control_frame_view, text="Amount:").grid(row=4, column=0)
        amount_entry = ttk.Entry(self.control_frame_view)
        amount_entry.insert(0, "00.00")  # Set initial text
        amount_entry.bind("<FocusIn>", lambda event: amount_entry.delete(0, "end"))  # Remove text on focus
        amount_entry.grid(row=4, column=1)
        def submit_transfer():
            from_account = combo_a.get()
            to_account = combo_b.get()
            transfer_date = transfer_date_entry.get()
            note = note_entry.get()
            amount = float(amount_entry.get())
            category = "transfer"
            # Call the Controller's method to handle the transfer submission
            self.Controller.Create_transfer(from_account, to_account, transfer_date, note, amount)

            
            # Show a label over the Submit button
            submit_label = ttk.Label(self.control_frame_view, text="Transfer submitted successfully!")
            submit_label.grid(row=5, column=1)

            # Schedule a function to hide the label after 2 seconds
            self.root.after(2000, submit_label.grid_forget)

            self.custom_month_budget_table_frame(transfer_date)
            reset_list()
            
            # Clear the input fields
            combo_a.set("")  # Clear the current selection
            combo_b.set("")
            transfer_date_entry.delete(0,tk.END)
            transfer_date_entry.insert(0,"YYYY-MM-DD")
            note_entry.delete(0, tk.END)
            note_entry.insert(0, "ABC...")
            amount_entry.delete(0, tk.END)
            amount_entry.insert(0, "00.00")

        # Create a submit button
        submit_button = ttk.Button(self.control_frame_view, text="Submit", command=submit_transfer)
        submit_button.grid(row=5)

        
    def create_income_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()
        self.control_frame_view.config(text="Income Form", bg="#9cbce4")

        
        ttk.Label(self.control_frame_view, text="Date: ").grid(row=1, column=0)
        income_date_entry = ttk.Entry(self.control_frame_view)
        income_date_entry.insert(0, "YYYY-MM-DD")  # Set initial text
        income_date_entry.bind("<FocusIn>", lambda event: income_date_entry.delete(0, "end"))  # Remove text on focus
        income_date_entry.grid(row=1, column=1)

        ttk.Label(self.control_frame_view, text="Note:").grid(row=2, column=0)
        note_entry = ttk.Entry(self.control_frame_view)
        note_entry.insert(0, "ABC...") #Set initial text
        note_entry.bind("<FocusIn>", lambda event: note_entry.delete(0,"end")) # remove text on key release
        note_entry.grid(row=2, column=1)

        ttk.Label(self.control_frame_view, text="Amount:").grid(row=3, column=0)
        amount_entry = ttk.Entry(self.control_frame_view)
        amount_entry.insert(0, "00.00") #set initial text
        amount_entry.bind("<FocusIn>", lambda event: amount_entry.delete(0, "end")) #remove text on focus
        amount_entry.grid(row=3, column=1)

        categories = self.get_sub_category_list()
        
        categories = [category for category in categories if category not in ['Expense', 'Transfer','Out Transfer','Fixed Expense','Going out','School','Food','Taxes','Other']]
        
        # Find the length of the longest date string in dates_list
        longest_category_length = max([len(category) for category in categories])
        
        ttk.Label(self.control_frame_view, text="Select Category :-").grid(row=4, column=0)
        from_dropdown = ttk.Combobox(self.control_frame_view, textvariable=self.sub_category, values=categories, width=longest_category_length)
        from_dropdown.grid(row=4, column=1, sticky="ew")
        
        def submit_income():
            income_date = income_date_entry.get()
            note = note_entry.get()
            amount = float(amount_entry.get())
            category = "Income"  
            # Call the Controller's method to handle the income submission
            self.Controller.add_transaction(income_date, note, amount, category)
            # Clear the input fields
            income_date_entry.delete(0, ttk.END)
            note_entry.delete(0, ttk.END)
            amount_entry.delete(0, ttk.END)
            
            # Show a label over the Submit button
            submit_label = ttk.Label(self.control_frame_view, text="Income submitted successfully!")
            submit_label.grid(row=5, column=1)

            # Schedule a function to hide the label after 2 seconds
            self.root.after(2000, submit_label.grid_forget)

            # Clear the entry fields
            income_date_entry.delete(0, 'end')
            note_entry.delete(0, 'end')
            amount_entry.delete(0, 'end')
            
            self.custom_month_budget_table_frame(income_date)
        
        # Create a submit button
        submit_button = ttk.Button(self.control_frame_view, text="Submit", command=submit_income)
        submit_button.grid(row=5)
        
        
        
        # Add relevant input fields and buttons for transfer screen
    def create_expense_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()
        self.control_frame_view.config(text="Expense Form", bg="#9cbce4")

        ttk.Label(self.control_frame_view, text="Date: ").grid(row=1, column=0)
        expense_date_entry = ttk.Entry(self.control_frame_view)
        expense_date_entry.insert(0, "YYYY-MM-DD")  # Set initial text
        expense_date_entry.bind("<FocusIn>", lambda event: expense_date_entry.delete(0, "end"))  # Remove text on focus
        expense_date_entry.grid(row=1, column=1)

        ttk.Label(self.control_frame_view, text="Note:").grid(row=2, column=0)
        note_entry = ttk.Entry(self.control_frame_view)
        note_entry.insert(0, "ABC...")  # Set initial text
        note_entry.bind("<FocusIn>", lambda event: note_entry.delete(0, "end"))  # Remove text on key release
        note_entry.grid(row=2, column=1)

        ttk.Label(self.control_frame_view, text="Amount:").grid(row=3, column=0)
        amount_entry = ttk.Entry(self.control_frame_view)
        amount_entry.insert(0, "00.00")  # Set initial text
        amount_entry.bind("<FocusIn>", lambda event: amount_entry.delete(0, "end"))  # Remove text on focus
        amount_entry.grid(row=3, column=1)
        
        categories = self.get_sub_category_list()
        
        categories = [category for category in categories if category not in ['Income', 'Expense', 'Transfer','Tax Refund','Refund']]
    
        recurring = ttk.BooleanVar()
        self.sub_category = ttk.StringVar()
        
        # Find the length of the longest date string in dates_list
        longest_category_length = max([len(category) for category in categories])
        
        ttk.Label(self.control_frame_view, text="Select Category :-").grid(row=4, column=0)
        from_dropdown = ttk.Combobox(self.control_frame_view, textvariable=self.sub_category, values=categories, width=longest_category_length)
        from_dropdown.grid(row=4, column=1, sticky="ew")
        
        self.fixed_expense = False
        def toggle_recurring():
            self.fixed_expense = True
            

        ttk.Label(self.control_frame_view, text="Recurring Expense:").grid(row=5, column=0)
        toggle_button = ttk.Checkbutton(self.control_frame_view, variable=recurring, command=toggle_recurring)
        toggle_button.grid(row=5, column=1)

        def submit_expense():
            expense_date = expense_date_entry.get()
            note = note_entry.get()
            amount = float(amount_entry.get())
            sub_category = self.sub_category
            if self.fixed_expense == True:
                category = "Fixed Expense"
                self.Controller.add_transaction(expense_date, note, amount, category,sub_category)
            else:
                category = "Expense"
                self.Controller.add_transaction(expense_date, note, amount, category)
            # Clear the input fields
            expense_date_entry.delete(0, ttk.END)
            note_entry.delete(0, ttk.END)
            amount_entry.delete(0, ttk.END)

            # Show a label over the Submit button
            submit_label = ttk.Label(self.control_frame_view, text="Expense submitted successfully!")
            submit_label.grid(row=6, column=1)

            # Schedule a function to hide the label after 2 seconds
            self.root.after(2000, submit_label.grid_forget)

            # Clear the entry fields
            expense_date_entry.delete(0, 'end')
            note_entry.delete(0, 'end')
            amount_entry.delete(0, 'end')

            self.custom_month_budget_table_frame(expense_date)

        # Create a submit button
        submit_button = ttk.Button(self.control_frame_view, text="Submit", command=submit_expense)
        submit_button.grid(row=6)


    def create_Edit_expense_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()
        self.control_frame_view.config(text="Edit expense Form", background="#4475b8")
        
        year = self.current_month_displayed.year
        month = self.current_month_displayed.month

        # Get the number of days in the month
        num_days = calendar.monthrange(year, month)[1]

        # Create a list to store the dates as strings
        dates_list = []

        # Iterate through the range of days and add each date to the list
        for day in range(1, num_days + 1):
            date_str = f"{year}-{month:02d}-{day:02d}"
            dates_list.append(date_str)
    
        look_up_date = tk.StringVar()
        # Find the length of the longest date string in dates_list
        longest_date_length = max([len(date) for date in dates_list])

        
        ttk.Label(self.control_frame_view, text="Date :").grid(row=0, column=0)
        from_dropdown = ttk.Combobox(self.control_frame_view, textvariable=look_up_date, values=dates_list, width=longest_date_length)
        from_dropdown.grid(row=0, column=1, sticky="ew")
        print(look_up_date)
        
        self.return_list = []
        def find_date():
            
            table_frame = ttk.Frame(self.control_frame_view)
            table_frame.grid(row=2, columnspan=4, sticky="ew")
            
            selected_date = look_up_date.get()
            self.return_list = self.Controller.look_up_expense(selected_date)
            
            for widget in table_frame.winfo_children():
                widget.destroy()
        
            if "None available" in self.return_list:
                tk.Label(table_frame, text="None available", justify='center').grid(row=1, column=0, columnspan=4)
                for widget in table_frame.winfo_children():
                    widget.destroy()
            else:
                labels = ["Date", "Account", "Note", "Amount", "Category"]
                for col, label in enumerate(labels):
                    ttk.Label(table_frame, text=label, relief=tk.SOLID, borderwidth=2).grid(row=1, column=col, sticky="ewns")

                data = self.return_list

                for row, entry_data in enumerate(data, start=3):
                    for col, value in enumerate(entry_data):
                        entry = ttk.Label(table_frame, text=value, width=10, justify='center', relief=tk.SOLID, borderwidth=2)
                        entry.grid(row=row, column=col, sticky="ewns")
        ttk.Button(self.control_frame_view, text="Look up", command=find_date).grid(row=0,column=3)
        
        

    #row 3 frame 2
    
    def monthly_overview(self, return_list):

        start_date = return_list[0][0]
        end_date = return_list[-1][0]
        
        start_checking = return_list[0][1]
        end_checking = return_list[-1][1]
        
        start_bailout = return_list[0][2]
        end_bailout = return_list[-1][2]
        
        start_saving = return_list[0][3]
        end_saving = return_list[-1][3]
        
        
        
        self.monthly_view = ttk.LabelFrame(self.frame2_control, text="Monthly view")
        self.monthly_view.grid(row=3, column=0, sticky="nsew", padx=10, pady=10) 
        
        ttk.Label(self.monthly_view, text=start_date).grid(row=0, column=0)
        ttk.Label(self.monthly_view, text=end_date).grid(row=0, column=3)
        # Align to bottom with padding
        ttk.Label(self.monthly_view, text="Accounts").grid(row=1, column=0,)
        ttk.Label(self.monthly_view, text="Starting Bal").grid(row=1, column=1,)
        ttk.Label(self.monthly_view, text="Ending Bal").grid(row=1, column=3,)
        
        ttk.Label(self.monthly_view, text="Checking").grid(row=2, column=0,)
        ttk.Label(self.monthly_view, text=start_checking).grid(row=2, column=1,)
        ttk.Label(self.monthly_view, text=end_checking).grid(row=2, column=3,)
        
        ttk.Label(self.monthly_view, text="Bail out").grid(row=3, column=0,)
        ttk.Label(self.monthly_view, text=start_bailout).grid(row=3, column=1,)
        ttk.Label(self.monthly_view, text=end_bailout).grid(row=3, column=3,)
        
        ttk.Label(self.monthly_view, text="Savings").grid(row=4, column=0,)
        ttk.Label(self.monthly_view, text=start_saving).grid(row=4, column=1,)
        ttk.Label(self.monthly_view, text=end_saving).grid(row=4, column=3,)
        

        
        
        #self.control_frame_view = tk.LabelFrame(self.frame2_control, text="Input area")
        #self.control_frame_view.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)  # Align to bottom with padding
        #tk.Label(self.control_frame_view, text="Text", width=20, padding=10).grid(row=1, column=0, rowspan=4, sticky="n")
        
if __name__ == "__main__":
    window = tk.Tk()
    app = BudgetApp(window)
    window.mainloop()
    
#source myenv/bin/activate