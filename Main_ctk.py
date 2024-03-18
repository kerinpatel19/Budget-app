import customtkinter as ctk
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg

from controller import Controller

class Driver(ctk.CTk):
    
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(size)
        self.main_frame = Main_frame(self)   
        
        #place them on the screen 
        self.main_frame.pack( fill='both', expand=True)
        self.current = datetime.now()
        self.current_month_displayed = self.current
        #self.mainloop()
        # Adjust the app size to fit the content
        self.update_idletasks()
        self.geometry(f"{self.winfo_reqwidth()}x{self.winfo_reqheight()}")
        

    
class Main_frame(ctk.CTkFrame):
    
        
    
    def __init__(self, parent):
        super().__init__(parent)
        self.accounts = ["Checking", "Bail out", "saving"]
        self.current = datetime.now()
        self.Controller = Controller()  
        self.Create_main_frames()
    

        self.current_month_displayed = self.current 
    def Create_main_frames(self):
        self.budget_table_frame = ctk.CTkFrame(self, fg_color="black")
        self.budget_table_frame.pack(side="left")
        
        self.Controls_frame = ctk.CTkFrame(self, fg_color="white")
        self.Controls_frame.pack(side="right", expand=True,fill="both")
        
        self.Create_all_frames()
        
    
    def Create_all_frames(self):
        
        self.monthly_view = ctk.CTkFrame(self.Controls_frame,  border_width = 1, border_color="Black", fg_color="#71ace3")
        self.monthly_view.grid(row=0, column=1, sticky="nsew",pady = 2, padx = 5, ipadx = 1, ipady = 1)
        
        self.Activity_frame = ctk.CTkFrame(self.Controls_frame, border_width = 2, border_color="Black", fg_color="#cadeef")
        self.Activity_frame.grid(row=1, column=1, sticky="nsew",pady = 2, padx = 5)
        
        self.control_frame = ctk.CTkFrame(self.Controls_frame,border_width = 1, border_color="Black", fg_color="#cadeef")
        self.control_frame.grid(row=2, column=1, sticky="nsew",pady = 2, padx = 5)
        
        self.control_frame_view = ctk.CTkFrame(self.Controls_frame, border_width = 1, border_color="Black", fg_color="#cadeef")
        self.control_frame_view.grid(row=3, column=1, sticky="nsew",pady = 2, padx = 5)
        
        
        
        self.create_control_buttons_frame()
        self.default_input_area_screen()
        self.current_month_budget_table_frame()
    
    def clear_budget_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.budget_table_frame.winfo_children():
            widget.destroy()
        
    
    def custom_month_budget_table_frame(self, date):
        self.clear_budget_screen()
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        self.current_month_displayed = date_obj
        custom_year = self.current_month_displayed.year
        custom_month= self.current_month_displayed.strftime("%B")
        return_list = self.Controller.update_table(custom_month,custom_year)
        
        labels = [" Date ", " Main ", " Bail-Out "," Saving ", 
                " transfer-out ", " transfer-In ",
                " Income ", " Expense "]
        for col, label in enumerate(labels):
            ctk.CTkLabel(self.budget_table_frame, text=label,
                            justify='center',
                            fg_color="#0784b5",
                            width=95,
                            text_color = "black",
                            padx = 2
                            ).grid(row=2, column=col, sticky="ewns")
            

        data = return_list
        
        scroll_frame = ctk.CTkScrollableFrame(self.budget_table_frame, width=740, height=850)
        scroll_frame.grid(row=3, column=0, columnspan = 8, sticky="ew")
        for row, entry_data in enumerate(data, start=3):
            # Alternate text color for each row
            fg_color = "#bebec2" if row % 2 == 0 else "#71ace3"
            for col, value in enumerate(entry_data):
                entry = ctk.CTkLabel(scroll_frame,
                                        text=value,
                                        width=94,
                                        justify='center',
                                        fg_color=fg_color,
                                        text_color = "black")
                entry.grid(row=row, column=col, sticky="nwes")
        self.monthly_overview(return_list)
    

    def current_month_budget_table_frame(self):
        self.clear_budget_screen()
        self.current_month_displayed = self.current
        date = datetime.strftime(self.current, "%Y-%m-%d")
        self.custom_month_budget_table_frame(date)       
    def last_month_budget_table_frame(self):
        
        self.clear_budget_screen()
        previous_month = self.current_month_displayed - relativedelta(months=1)
        self.current_month_displayed = previous_month
        date = datetime.strftime(previous_month, "%Y-%m-%d")
        self.custom_month_budget_table_frame(date)
    def next_month_budget_table_frame(self):
        self.clear_budget_screen()

        next_month = self.current_month_displayed + relativedelta(months=1)
        self.current_month_displayed = next_month
        date = datetime.strftime(next_month, "%Y-%m-%d")
        self.custom_month_budget_table_frame(date)
        
    def create_control_buttons_frame(self):
        #fg_color = "#bebec2" if row % 2 == 0 else "#71ace3"
        background = "#39ace7"
        text_Color = "black"
        hover_color = "#9bd4e4"
        border_Width = 2
        border_Color = "black"
        width = 2

        ctk.CTkButton(self.control_frame, text="Transfer", width=width,
                        command= self.create_transfer_screen,
                        border_width = border_Width,
                        border_color=border_Color,
                        text_color=text_Color,
                        hover_color=hover_color,
                        fg_color=background).grid(row=0, column=0, columnspan=1, rowspan=1, sticky="ew")
        ctk.CTkButton(self.control_frame, text="Add Income", width=width,hover_color=hover_color,
                        command= self.create_income_screen,border_width = border_Width,
                        border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=0, column=1, columnspan=1, rowspan=1, sticky="ew")
        ctk.CTkButton(self.control_frame, text="Expense", width=width,hover_color=hover_color,
                        command=self.create_expense_screen,border_width = border_Width,
                        border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=0, column=2, columnspan=1, rowspan=1, sticky="ew")
        
        ctk.CTkButton(self.control_frame, text="last month",command=self.last_month_budget_table_frame,hover_color=hover_color,
                        border_width = border_Width, border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=1, column=0, columnspan=1, rowspan=1, sticky="wen")
        ctk.CTkButton(self.control_frame, text="Current month",command=self.current_month_budget_table_frame,hover_color=hover_color,
                        border_width = border_Width, border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=1, column=1, columnspan=1, rowspan=1, sticky="ew")
        ctk.CTkButton(self.control_frame, text="Next month",command=self.next_month_budget_table_frame,hover_color=hover_color,
                        border_width = border_Width, border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=1,column=2, columnspan=1, rowspan=1, sticky="wen")

        ctk.CTkButton(self.control_frame, text="scan statement",border_width = border_Width,hover_color=hover_color,
                        border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=2, column=0, columnspan=1, rowspan=1, sticky="ewn")
        ctk.CTkButton(self.control_frame, text="Add more year",border_width = border_Width,hover_color=hover_color,
                        border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=2, column=1, columnspan=1, rowspan=1, sticky="ew")
        ctk.CTkButton(self.control_frame, text="Add Category",border_width = border_Width,hover_color=hover_color,
                        border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=2,column=2, columnspan=1, rowspan=1, sticky="ewn")
        
    
    def get_sub_category_list(self):
        return_list = self.Controller.sub_category()
        return return_list
    #row 2   frame 2  
    def default_input_area_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()

        sizes = [10, 20, 30, 40]  # example data
        labels = ['A', 'B', 'C', 'D']  # example labels
        explode = (0, 0.0, 0, 0)  # "explode" the 2nd slice (i.e. 'B')

        fig, ax = plt.subplots(figsize=(1, 1))  # Set the size to 6x6 inches
        ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90,)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

        canvas = tkagg.FigureCanvasTkAgg(fig, self.control_frame_view)
        canvas.get_tk_widget().grid(row=2, column=1, sticky="nesw")
        self.control_frame_view.grid(row=3, column=1, sticky="nesw")

        

    def create_transfer_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()

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
        #right side
        text_color2 = "white"        
                
    
        #left side
        background = "#39ace7"
        text_color = "black"
        
        
        ctk.CTkLabel(self.control_frame_view, text="Transfer Form", fg_color="#0784b5", text_color=text_color,height= 10, width=200).grid(row=0, column=0,columnspan = 8,sticky="we")
        
        ctk.CTkLabel(self.control_frame_view, text="From Account:", text_color=text_color, fg_color=background,corner_radius = 2).grid(row=2, column=0,columnspan = 4,sticky="we")
        combo_a = ctk.CTkComboBox(self.control_frame_view, values=self.accounts)
        combo_a.grid(row=2, column=4)
        combo_a.bind("<<ComboboxSelected>>", update_to_options)


        ctk.CTkLabel(self.control_frame_view, text="To Account:", text_color=text_color, fg_color=background, corner_radius = 2).grid(row=4, column=0, columnspan = 4,sticky="we")
        combo_b = ctk.CTkComboBox(self.control_frame_view, values=self.accounts)
        combo_b.grid(row=4, column=4)
        combo_b.bind("<<ComboboxSelected>>", update_to_options)



        ctk.CTkLabel(self.control_frame_view, text="Date: ", text_color=text_color, fg_color=background, corner_radius = 2).grid(row=6, column=0,columnspan = 4,sticky="we")
        transfer_date_entry = ctk.CTkEntry(self.control_frame_view ,text_color=text_color2)
        transfer_date_entry.insert(0, "YYYY-MM-DD")  # Set initial text
        transfer_date_entry.bind("<FocusIn>", lambda event: transfer_date_entry.delete(0, "end"))  # Remove text on focus
        transfer_date_entry.grid(row=6, column=4)

        ctk.CTkLabel(self.control_frame_view, text="Note:",  text_color=text_color, fg_color=background, corner_radius = 2).grid(row=8, column=0,columnspan = 4,sticky="we")
        note_entry = ctk.CTkEntry(self.control_frame_view,text_color=text_color2)
        note_entry.insert(0, "ABC...")  # Set initial text
        note_entry.bind("<FocusIn>", lambda event: note_entry.delete(0, "end"))  # Remove text on key release
        note_entry.grid(row=8, column=4)

        ctk.CTkLabel(self.control_frame_view, text="Amount:",  text_color=text_color, fg_color=background, corner_radius = 2).grid(row=10, column=0,columnspan = 4,sticky="we")
        amount_entry = ctk.CTkEntry(self.control_frame_view,text_color=text_color2)
        amount_entry.insert(0, "00.00")  # Set initial text
        amount_entry.bind("<FocusIn>", lambda event: amount_entry.delete(0, "end"))  # Remove text on focus
        amount_entry.grid(row=10, column=4)
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
            submit_label = ctk.CTkLabel(self.control_frame_view, text="Transfer submitted successfully!", text_color="black")
            submit_label.grid(row=14, column=1)

            self.custom_month_budget_table_frame(transfer_date)

            reset_list()
            
            # Clear the input fields
            combo_a.set("")  # Clear the current selection
            combo_b.set("")
            transfer_date_entry.delete(0,ctk.END)
            transfer_date_entry.insert(0,"YYYY-MM-DD")
            note_entry.delete(0, ctk.END)
            note_entry.insert(0, "ABC...")
            amount_entry.delete(0, ctk.END)
            amount_entry.insert(0, "00.00")

        # Create a submit button
        submit_button = ctk.CTkButton(self.control_frame_view, text="Submit", command=submit_transfer)
        submit_button.grid(row=12, column=0,columnspan = 4, sticky="we")
    def create_income_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()
        
        #right side
        text_color2 = "white"        
                
    
        #left side
        background = "#39ace7"
        text_color = "black"

        ctk.CTkLabel(self.control_frame_view, text="Income Form", fg_color="#0784b5", text_color=text_color,height= 10, width=200).grid(row=0, column=0,columnspan = 8,sticky="we")
        
        ctk.CTkLabel(self.control_frame_view, text="Date: ", text_color=text_color, fg_color=background, corner_radius = 2).grid(row=6, column=0,columnspan = 4,sticky="we")
        income_date_entry = ctk.CTkEntry(self.control_frame_view ,text_color=text_color2)
        income_date_entry.insert(0, "YYYY-MM-DD")  # Set initial text
        income_date_entry.bind("<FocusIn>", lambda event: income_date_entry.delete(0, "end"))  # Remove text on focus
        income_date_entry.grid(row=6, column=4)

        ctk.CTkLabel(self.control_frame_view, text="Note:",  text_color=text_color, fg_color=background, corner_radius = 2).grid(row=8, column=0,columnspan = 4,sticky="we")
        note_entry = ctk.CTkEntry(self.control_frame_view,text_color=text_color2)
        note_entry.insert(0, "ABC...")  # Set initial text
        note_entry.bind("<FocusIn>", lambda event: note_entry.delete(0, "end"))  # Remove text on key release
        note_entry.grid(row=8, column=4)

        ctk.CTkLabel(self.control_frame_view, text="Amount:",  text_color=text_color, fg_color=background, corner_radius = 2).grid(row=10, column=0,columnspan = 4,sticky="we")
        amount_entry = ctk.CTkEntry(self.control_frame_view,text_color=text_color2)
        amount_entry.insert(0, "00.00")  # Set initial text
        amount_entry.bind("<FocusIn>", lambda event: amount_entry.delete(0, "end"))  # Remove text on focus
        amount_entry.grid(row=10, column=4)

        categories = self.get_sub_category_list()
        
        categories = [category for category in categories if category not in ['Expense', 'In Transfer','Out Transfer','Fixed Expense','Going out','School','Food','Taxes','Other']]
        
        # Find the length of the longest date string in dates_list
        longest_category_length = max([len(category) for category in categories])
        
        ctk.CTkLabel(self.control_frame_view, text="Select Category :-",  text_color=text_color, fg_color=background, corner_radius = 2).grid(row=12, column=0,columnspan = 4,sticky="we")
        from_dropdown = ctk.CTkComboBox(self.control_frame_view, values=categories, width=longest_category_length)
        from_dropdown.grid(row=12, column=4, sticky="ew")
        
        def submit_income():
            income_date = income_date_entry.get()
            note = note_entry.get()
            amount = float(amount_entry.get())
            category = "Income"  
            sub_category = from_dropdown.get()
            # Call the Controller's method to handle the income submission
            self.Controller.add_transaction(income_date, note, amount, category, sub_category)
            # Clear the input fields
            income_date_entry.delete(0, ctk.END)
            note_entry.delete(0, ctk.END)
            amount_entry.delete(0, ctk.END)
            
            # Show a label over the Submit button
            income_label = ctk.CTkLabel(self.control_frame_view, text="Transfer submitted successfully!", text_color="black")
            income_label.grid(row=18, column=1)

            # Clear the entry fields
            income_date_entry.delete(0, 'end')
            note_entry.delete(0, 'end')
            amount_entry.delete(0, 'end')
            
            income_date_entry.delete(0,ctk.END)
            income_date_entry.insert(0,"YYYY-MM-DD")
            note_entry.delete(0, ctk.END)
            note_entry.insert(0, "ABC...")
            amount_entry.delete(0, ctk.END)
            amount_entry.insert(0, "00.00")
            # Wait for a few seconds before destroying the successful message
            self.control_frame_view.after(3000, lambda: income_label.destroy())
            
            self.custom_month_budget_table_frame(income_date)
        
        # Create a submit button
        submit_button = ctk.CTkButton(self.control_frame_view, text="Submit", command=submit_income)
        submit_button.grid(row=16, column=0,columnspan = 4, sticky="we")
        
        
        
        # Add relevant input fields and buttons for transfer screen
    def create_expense_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()
        
        #right side
        text_color2 = "white"        
                
    
        #left side
        background = "#39ace7"
        text_color = "black"

        ctk.CTkLabel(self.control_frame_view, text="Expense Form", fg_color="#0784b5", text_color=text_color,height= 10, width=200).grid(row=0, column=0,columnspan = 8,sticky="we")
        
        ctk.CTkLabel(self.control_frame_view, text="Date: ", text_color=text_color, fg_color=background, corner_radius = 2).grid(row=6, column=0,columnspan = 4,sticky="we")
        expense_date_entry = ctk.CTkEntry(self.control_frame_view ,text_color=text_color2)
        expense_date_entry.insert(0, "YYYY-MM-DD")  # Set initial text
        expense_date_entry.bind("<FocusIn>", lambda event: expense_date_entry.delete(0, "end"))  # Remove text on focus
        expense_date_entry.grid(row=6, column=4)

        ctk.CTkLabel(self.control_frame_view, text="Note:",  text_color=text_color, fg_color=background, corner_radius = 2).grid(row=8, column=0,columnspan = 4,sticky="we")
        note_entry = ctk.CTkEntry(self.control_frame_view,text_color=text_color2)
        note_entry.insert(0, "ABC...")  # Set initial text
        note_entry.bind("<FocusIn>", lambda event: note_entry.delete(0, "end"))  # Remove text on key release
        note_entry.grid(row=8, column=4)

        ctk.CTkLabel(self.control_frame_view, text="Amount:",  text_color=text_color, fg_color=background, corner_radius = 2).grid(row=10, column=0,columnspan = 4,sticky="we")
        amount_entry = ctk.CTkEntry(self.control_frame_view,text_color=text_color2)
        amount_entry.insert(0, "00.00")  # Set initial text
        amount_entry.bind("<FocusIn>", lambda event: amount_entry.delete(0, "end"))  # Remove text on focus
        amount_entry.grid(row=10, column=4)
        
        categories = self.get_sub_category_list()
        
        categories = [category for category in categories if category not in ['Income', 'Expense', 'In Transfer','Out Transfer','Tax Refund','Refund']]
    
        recurring = ctk.BooleanVar()
        self.sub_category = ctk.StringVar()
        
        # Find the length of the longest date string in dates_list
        longest_category_length = max([len(category) for category in categories])
        
        ctk.CTkLabel(self.control_frame_view, text="Select Category :-",  text_color=text_color, fg_color=background, corner_radius = 2).grid(row=12, column=0,columnspan = 4,sticky="we")
        from_dropdown = ctk.CTkComboBox(self.control_frame_view, values=categories, width=longest_category_length)
        from_dropdown.grid(row=12, column=4, sticky="ew")
        
        self.fixed_expense = False
        def toggle_recurring():
            self.fixed_expense = True
            

        toggle_button = ctk.CTkCheckBox(self.control_frame_view, variable=recurring, command=toggle_recurring,text="Recurring Expense",fg_color=background,text_color=text_color)
        toggle_button.grid(row=14, column=0, columnspan=8)

        def submit_expense():
            expense_date = expense_date_entry.get()
            note = note_entry.get()
            amount = float(amount_entry.get())
            sub_category = self.sub_category.get()
            if self.fixed_expense == True:
                category = "Fixed Expense"
                self.Controller.add_transaction(expense_date, note, amount, category,sub_category)
            else:
                category = "Expense"
                self.Controller.add_transaction(expense_date, note, amount, category,sub_category)
                
            # Show a label over the Submit button
            expense_label = ctk.CTkLabel(self.control_frame_view, text="Transfer submitted successfully!", text_color="black")
            expense_label.grid(row=18, column=1)

            # Clear the entry fields
            expense_date_entry.delete(0, 'end')
            note_entry.delete(0, 'end')
            amount_entry.delete(0, 'end')
            
            expense_date_entry.delete(0,ctk.END)
            expense_date_entry.insert(0,"YYYY-MM-DD")
            note_entry.delete(0, ctk.END)
            note_entry.insert(0, "ABC...")
            amount_entry.delete(0, ctk.END)
            amount_entry.insert(0, "00.00")
            self.fixed_expense = False
            # Wait for a few seconds before destroying the successful message
            self.control_frame_view.after(3000, lambda: expense_label.destroy())

            self.custom_month_budget_table_frame(expense_date)

        # Create a submit button
        submit_button = ctk.CTkButton(self.control_frame_view, text="Submit", command=submit_expense)
        submit_button.grid(row=16, column=0,columnspan = 8, sticky="we")



    def monthly_overview(self, return_list):
        

        start_date = return_list[0][0]
        end_date = return_list[-1][0]
        
        start_checking = return_list[0][1]
        end_checking = return_list[-1][1]
        
        start_bailout = return_list[0][2]
        end_bailout = return_list[-1][2]
        
        start_saving = return_list[0][3]
        end_saving = return_list[-1][3]
        
        added_tranctions = []
        background = "#bebec2" #black
        background2 = "#71ace3" # light blue 
        background3 = "#39ace7" #bright blue 
        background4 = "#0784b5" # dark blue
        text_color = "black"
        width = 5
        height = 20
        radius=20
        side = "e"
        
        
        
        
        
        monthly_transfer_In = 0.0
        monthly_transfer_Out = 0.0
        monthly_income = 0.0
        monthly_expenses = 0.0
        # Iterate through the data list and sum up the expenses for each month
        for entry in return_list:
            
            expense = entry[-1]  # Get the expense from the last element of the entry
            income = entry[-2]
            transfer_in = entry[-3]
            transfer_out = entry[-4]
            
            # Add the expense to the monthly total for the corresponding year and month
            monthly_expenses += expense
            monthly_transfer_In += transfer_in
            monthly_transfer_Out += transfer_out
            monthly_income += income
                
        
        
        # Monthly Summary label
        ctk.CTkLabel(self.monthly_view, text="Monthly Summary", text_color=text_color,fg_color=background3, width=420,height= 30, justify="center", font=("arial", 15)).grid(row=0, column=0, columnspan=5, sticky="ew")

        ctk.CTkLabel(self.monthly_view, text=f"From - {start_date}\n   To - {end_date}", text_color=text_color, width=width, anchor="e", bg_color=background4,font=("arial", 13)).grid(row=1, column=0, sticky="ew")

        ctk.CTkLabel(self.monthly_view, text="Starting Balance", text_color=text_color, width=width,height=30, font=("arial", 10), anchor="se", bg_color=background4).grid(row=1, column=1, sticky="ew")
        ctk.CTkLabel(self.monthly_view, text="Ending Balance", text_color=text_color, width=width,height=30, font=("arial", 10),anchor="se", bg_color=background4).grid(row=1, column=2, sticky="ew")

        ctk.CTkLabel(self.monthly_view, text="", text_color=text_color, width=width,height=30, anchor="e", bg_color=background4,font=("arial", 13)).grid(row=1, column=3, sticky="ew", columnspan=2)

        # Account labels
        accounts = ["Checking", "Bail out", "Savings","Monthly Income","Monthly Expense","Monthly transfer In","Monthly transfer Out"]
        for idx, account in enumerate(accounts, start=2):
            ctk.CTkLabel(self.monthly_view, text=account,bg_color=background, text_color=text_color, width=width,height=height, justify="right", anchor=side).grid(row=idx, column=0, sticky="ew")

        # Starting balances
        starting_balances = [start_checking, start_bailout, start_saving,monthly_income,monthly_expenses,monthly_transfer_In,monthly_transfer_Out]
        for idx, balance in enumerate(starting_balances, start=2):
            # Alternate text color for each row
            ctk.CTkLabel(self.monthly_view, text=f"$ {balance}", text_color=text_color, width=width,height=height, justify="left",anchor=side).grid(row=idx, column=1, sticky="ew")

        # Ending balances
        ending_balances = [end_checking, end_bailout, end_saving]
        for idx, balance in enumerate(ending_balances, start=2):
            ctk.CTkLabel(self.monthly_view, text=f"$ {balance}", text_color=text_color, width=width,height=height, justify="left",anchor=side).grid(row=idx, column=2, sticky="ew")
        
        self.activity_view(start_date)
        
    def view_expense(self, start_date, subcategory):
        
        # Clear existing content of control_frame_view
        for widget in self.Activity_frame.winfo_children():
            widget.destroy()
        
        return_list_expense = self.Controller.look_up_expense(start_date, subcategory)
        
        
        scrollable_frame = ctk.CTkScrollableFrame(self.Activity_frame, width=400, height=200)
        scrollable_frame.pack()
        
        labels = ["Transaction Date", "Account", "Note", "Amount","Sub_Category"]
        for col, label in enumerate(labels):
            ctk.CTkLabel(scrollable_frame, text=label,
                        justify='center',
                        fg_color="#0784b5",
                        
                        text_color="black"
                        ).grid(row=2, column=col, sticky="ewns", padx=1)
        
        data = return_list_expense
        for row, entry_data in enumerate(data, start=3):
            # Alternate text color for each row
            fg_color = "#bebec2" if row % 2 == 0 else "#71ace3"
            
            for col, value in enumerate(entry_data):
                entry = ctk.CTkLabel(scrollable_frame, text=value, width=10, justify='center', fg_color=fg_color, text_color="black")
                entry.grid(row=row, column=col, sticky="nwes",padx=1)
        
        
        background = "#39ace7"
        text_Color = "black"
        hover_color = "#9bd4e4"
        border_Width = 2
        border_Color = "black"
        width = 2
        
        def summit():
            self.activity_view(start_date)
        
        ctk.CTkButton(self.Activity_frame, text="Go Back",
                    fg_color=background,
                    text_color=text_Color,
                    hover_color=hover_color,
                    border_width=border_Width,
                    border_color=border_Color,
                    command=summit
                    ).pack()

        
        
        
    def activity_view(self, start_date):
        # Clear existing content of control_frame_view
        for widget in self.Activity_frame.winfo_children():
            widget.destroy()
            
        sub_catogeiors = self.get_sub_category_list()
        tab_amount = len(sub_catogeiors)
        background = "#bebec2" #black
        background2 = "#71ace3" # light blue 
        background3 = "#39ace7" #bright blue 
        background4 = "#0784b5" # dark blue
        text_Color = "black"
        hover_color = "#9bd4e4"
        border_Width = 2
        border_Color = "black"
        width = 2
        def summit(subcategory):
            date = datetime.strftime(self.current_month_displayed,"%Y-%m-%d")
            self.view_expense(date, subcategory)
        y_offset = 0  # Initial y-coordinate offset
        for idx, subcategory in enumerate(sub_catogeiors):
            return_list_expense = self.Controller.look_up_expense(start_date, subcategory)
            total_amount = 0.0
            for item in return_list_expense:
                total_amount += item[3]  # Add the amount from each sublist to the total


            label_1 = ctk.CTkLabel(self.Activity_frame, text=f"{subcategory}", width=100, bg_color=background4, text_color=text_Color)
            label_1.grid(row=idx, column=0, sticky="ew")
            
            label_2 = ctk.CTkLabel(self.Activity_frame, text=f"Amount - ${total_amount}\t", width=180, bg_color=background, fg_color=background, anchor="e", text_color=text_Color)
            label_2.grid(row=idx, column=1, sticky="ew")
            
            view_button = ctk.CTkButton(self.Activity_frame, text="View Transactions", bg_color=background3,
                                        fg_color=background2,
                                        text_color=text_Color,
                                        hover_color=hover_color,
                                        border_width=border_Width,
                                        border_color=border_Color,
                                        command=lambda subcategory=subcategory: summit(subcategory)
                                        )
            view_button.grid(row=idx, column=2, sticky="ew")

            y_offset += 30  # Increase the y-coordinate offset for the next widget
Driver('Budget app', '600x600').mainloop()


#source myenv/bin/activate