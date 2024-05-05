import customtkinter as ctk
from customtkinter import filedialog 
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math
from controller import Controller
from PIL import Image, ImageTk

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
        #self.resizable(False, False)
        self.new_category = None

class Main_frame(ctk.CTkFrame):
    
        
    
    def __init__(self, parent):
        super().__init__(parent)
        self.accounts = ["Checking", "Bail out", "saving"]
        self.current = datetime.now()
        self.current_month_displayed = self.current
        self.Controller = Controller()  
        self.Create_main_frames()
        self.sub_category = []
        self.new_category = None


    def Create_main_frames(self):
        self.budget_table_frame = ctk.CTkFrame(self, fg_color="black")
        self.budget_table_frame.pack(side="left", expand=True,fill="both")
        
        self.Controls_frame = ctk.CTkFrame(self, fg_color="black")
        self.Controls_frame.pack(side="right", expand=True,fill="both")
        
        self.Create_all_frames()
        
    
    def Create_all_frames(self):
        
        self.monthly_view = ctk.CTkFrame(self.Controls_frame,  border_width = 1, border_color="Black", fg_color="#bebec2")
        self.monthly_view.pack(fill="x", ipadx = 1, ipady = 1)
        
        self.Activity_frame = ctk.CTkFrame(self.Controls_frame, border_width = 2, border_color="Black", fg_color="#cadeef")
        self.Activity_frame.pack(fill="both", ipadx = 1, ipady = 1, expand=True)
        
        self.control_frame = ctk.CTkFrame(self.Controls_frame,border_width = 1, border_color="Black", fg_color="#cadeef", bg_color="black")
        self.control_frame.pack(fill="x", ipadx = 1, ipady = 1)
        
        self.control_frame_view = ctk.CTkFrame(self.Controls_frame, border_width = 1, border_color="Black", fg_color="#cadeef")
        self.control_frame_view.pack(fill="both", ipadx = 1, ipady = 1)
        
        
        
        self.create_control_buttons_frame()
        self.todays_expense_screen()
        self.current_month_budget_table_frame()
    
    def clear_budget_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.budget_table_frame.winfo_children():
            widget.destroy()
            
    def add_year_fail_safe(self, year,date):
        self.add_year(year)
        self.custom_month_budget_table_frame(date)
        self.todays_expense_screen()
        self.current_month_budget_table_frame()
    
    def custom_month_budget_table_frame(self, date):
        self.clear_budget_screen()
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        self.current_month_displayed = date_obj
        custom_year = self.current_month_displayed.year
        custom_month= self.current_month_displayed.strftime("%B")
        return_list = self.Controller.update_table(custom_month,custom_year)
        if return_list == ["No data found"]:
            ctk.CTkLabel(self.budget_table_frame, text="Not In that year yet. - Add more years",
                                justify='center',
                                fg_color="#0784b5",
                                text_color = "black",
                                padx = 2
                                ).grid(row=2, column=1,columnspan=8 , sticky="ewns")
            self.add_year_fail_safe(f'{custom_year}',date)
            
        else:
            labels = [" Date ", " Main ", " Bail-Out "," Saving "," transfer-out ", " transfer-In "," Income ", " Expense "]
            for col, label in enumerate(labels):
                ctk.CTkLabel(self.budget_table_frame, text=label,
                                justify='center',
                                fg_color="#0784b5",
                                width=95,
                                text_color = "black",
                                padx = 2
                                ).grid(row=2, column=col, sticky="ewns")
                

            data = return_list
            
            scroll_frame = ctk.CTkScrollableFrame(self.budget_table_frame, width=500, height=800)
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
                    entry.grid(row=row, column=col, sticky="nwes",pady = 1)
            self.monthly_overview(return_list)
    
    def view_expense_list(self, return_list):
        self.clear_budget_screen()
        Expense_list_frame = ctk.CTkScrollableFrame(self.budget_table_frame, 
                                            width=740,
                                            height=800)
        Expense_list_frame.grid(row=0, column=0)
        expense_counter = 0
        sub_category_expense = self.get_sub_category_list("Expense")
        sub_category_income = self.get_sub_category_list("Income")
        def combobox_callback(choice):
            self.new_category = choice
            Update_button.configure(state="normal")
        
        r = 0
        c = 0
        
        for i in range(len(return_list)):
            
            frame = ctk.CTkFrame(Expense_list_frame,
                                    border_width= 2,
                                    border_color= "black",
                                    fg_color="#bebec2",
                                    )
            frame.grid(row = r, column = c, ipady = 4, ipadx = 4, padx = 4, pady= 4, sticky="ewns")
            if c == 1:
                r += 1
                c = 0
            else:
                c += 1
            labels = ["Transaction Date", "Account", "Note", "Amount","Sub Category"]
            data = [
                    return_list[i][1],
                    return_list[i][2],
                    return_list[i][3],
                    return_list[i][4],
                    ]
            ctk.CTkLabel(frame,
                            text=f"Transaction ID  - ",
                            fg_color= "#0784b5", # dark blue
                            bg_color="transparent",
                            anchor="e",
                            text_color="black").grid(row=0, column=0, sticky="ew", pady=5)
            ctk.CTkLabel(frame,
                            text=return_list[i][0],
                            fg_color= "#0784b5", # dark blue
                            bg_color="transparent",
                            anchor="w",
                            text_color="black",).grid(row=0, column=1, sticky="ew", pady=5)

            for i in range(len(labels)):
                ctk.CTkLabel(frame,
                                text=f"{labels[i]}",
                                fg_color="#71ace3",#light blue,
                                bg_color="transparent",
                                anchor="center",
                                text_color="black").grid(row=i + 1, column=0, sticky="ewns", padx=5, pady=2)
            for i in range(4):
                ctk.CTkLabel(frame,
                                text=data[i],
                                fg_color="#bebec2",#grey
                                bg_color="transparent",
                                anchor="w",
                                text_color="black",wraplength=150).grid(row=i + 1, column=1, sticky="ew", padx=5, pady=2)
                
            sub_category = None
                
            if return_list[expense_counter][5] == "Transfer IN":
                sub_category = sub_category_income
            elif return_list[expense_counter][5] == "Transfer OUT":
                sub_category = sub_category_expense
            elif return_list[expense_counter][5] == "Expense-Unsorted":
                sub_category = sub_category_expense
            elif return_list[expense_counter][5] == "Income-Unsorted":
                sub_category = sub_category_income
            elif return_list[expense_counter][5] in sub_category_income:
                sub_category = sub_category_income
            elif return_list[expense_counter][5] in sub_category_expense:
                sub_category = sub_category_expense
            else:
                print("none found", return_list[expense_counter][5])

            category_select = ctk.CTkComboBox(frame, values=sub_category,
                                        command=combobox_callback)
            category_select.grid(row=i + 2, column = 1, sticky="w")
            category_select.set(return_list[expense_counter][5])
            # Edit Button
            Delete_button = ctk.CTkButton(frame, text="Delete", command=lambda f=frame: self.delete_expense(f))
            Delete_button.grid(row=i + 3, column=0, columnspan =1, rowspan = 1, sticky="wesn",pady=1, padx = 5)
            Update_button = ctk.CTkButton(frame, text="Update", command=lambda f=frame: self.update_expense(f), state="disabled")
            Update_button.grid(row=i + 3, column=1, columnspan =1, rowspan = 1, sticky="wesn",pady=1, padx = 5)
            print("bank verified - ",return_list[expense_counter][6])
            if int(return_list[expense_counter][6]) == 1:
                # Load the image
                image_path = "/Users/kerinpatel/Desktop/Projects-python/Budget-app/images/bank_verified.png"
                
                image = ctk.CTkImage(Image.open(image_path), size=(26, 26))
                # Create a ctk Label widget to display the image
                label = ctk.CTkLabel(frame, image= image, anchor="e", text="", fg_color="transparent")

                # Display the label
                label.grid(row=0, column=1, sticky="ew", pady=5)
                print("placed")
            
        expense_counter += 1

        def go_back():
            date = datetime.strftime(self.current_month_displayed,'%Y-%m-%d')
            self.custom_month_budget_table_frame(date)
        Go_back_button = ctk.CTkButton(self.budget_table_frame, text="Go back",
                                                command=go_back)
        Go_back_button.grid(row=1, column=0, sticky="wesn")
    def update_expense(self, frame):
        # Extract data from the frame
        transaction_ID = frame.grid_slaves(row=0, column=1)[0].cget("text")
        transaction_date = frame.grid_slaves(row=0, column=1)[0].cget("text")
        date = datetime.strptime(transaction_date,"%Y-%m-%d")
        year = int(date.year)
        message = self.Controller.Update_expense(transaction_ID,transaction_date,self.new_category,year)
        for widget in frame.winfo_children():
            widget.destroy()
        # Show a label over the Submit button
        label = ctk.CTkLabel(frame, text=message, text_color="black", anchor= "center")
        label.pack(fill = "x", padx = 5, ipady = 5,ipadx = 5)
    def delete_expense(self, frame):
        # Extract data from the frame
        transaction_ID = frame.grid_slaves(row=0, column=1)[0].cget("text")
        transaction_date = frame.grid_slaves(row=1, column=1)[0].cget("text")
        date = datetime.strptime(transaction_date,"%Y-%m-%d")
        year = int(date.year)
        message = self.Controller.delete_expense_row(transaction_ID, transaction_date,year)
        # Clear existing content of control_frame_view
        for widget in frame.winfo_children():
            widget.destroy()
        # Show a label over the Submit button
        label = ctk.CTkLabel(frame, text=message, text_color="black", anchor= "center")
        label.pack(fill = "x", padx = 5, ipady = 5,ipadx = 5)
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
    
    def settings_function_view(self):
        background = "#39ace7"
        text_Color = "black"
        hover_color = "#9bd4e4"
        border_Width = 2
        border_Color = "black"
        width = 2
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()
        
        scrollable_frame = ctk.CTkScrollableFrame(self.control_frame_view)
        scrollable_frame.pack(fill="both")
        
        ctk.CTkButton(scrollable_frame, text="Delete Year", command=self.delete_year_screen,border_width = border_Width,hover_color=hover_color,
                        border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=0, column=0, columnspan=1, rowspan=1, sticky="ewn")
        ctk.CTkButton(scrollable_frame, text="Add Starting balance", command=self.Add_starting_balance_screen,border_width = border_Width,hover_color=hover_color,
                        border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=0, column=1, columnspan=1, rowspan=1, sticky="ew")
        ctk.CTkButton(scrollable_frame, text="Delete Entry",border_width = border_Width,hover_color=hover_color,
                        border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=0,column=2, columnspan=1, rowspan=1, sticky="ewn")
        
        ctk.CTkButton(scrollable_frame, text="change database key",border_width = border_Width,hover_color=hover_color,
                        border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=1, column=0, columnspan=1, rowspan=1, sticky="ewn")
        ctk.CTkButton(scrollable_frame, text="Add data base",border_width = border_Width,hover_color=hover_color,
                        border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=1, column=1, columnspan=1, rowspan=1, sticky="ew")
        ctk.CTkButton(scrollable_frame, text="Refresh View",command = self.refresh_view,border_width = border_Width,hover_color=hover_color,
                        border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=1,column=2, columnspan=1, rowspan=1, sticky="ewn")
        def go_back():
            self.todays_expense_screen()
        ctk.CTkButton(scrollable_frame, text="Go back",command = go_back,border_width = border_Width,hover_color=hover_color,
                        border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=2,column=0, columnspan=1, rowspan=3, sticky="ewn")

    
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

        ctk.CTkButton(self.control_frame, text="scan statement",command=self.Scan_statement,border_width = border_Width,hover_color=hover_color,
                        border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=2, column=0, columnspan=1, rowspan=1, sticky="ewn")
        ctk.CTkButton(self.control_frame, text="Add more year",command=self.Add_year_scree,border_width = border_Width,hover_color=hover_color,
                        border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=2, column=1, columnspan=1, rowspan=1, sticky="ew")
        ctk.CTkButton(self.control_frame, text="Settings",command=self.settings_function_view,border_width = border_Width,hover_color=hover_color,
                        border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=2,column=2, columnspan=1, rowspan=1, sticky="ewn")
        
        
    
    def get_sub_category_list(self,Control_Category):
        return_list = self.Controller.sub_category(Control_Category)
        return return_list
    #row 2   frame 2  
    def todays_expense_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()
        date = datetime.strftime(self.current,"%Y-%m-%d")
        return_list_expense = self.Controller.look_up_expense_by_date(date)

        scrollable_frame = ctk.CTkScrollableFrame(self.control_frame_view)
        scrollable_frame.pack(fill="both")
        if return_list_expense != ["No expense"]:
            labels = ["Transaction Date", "Account", "Note", "Amount","Sub_Category"]
            for col, label in enumerate(labels):
                ctk.CTkLabel(scrollable_frame, text=label,
                            justify='center',
                            fg_color="#0784b5",
                            corner_radius = 2,
                            text_color="black"
                            ).grid(row=2, column=col, sticky="ewns", padx=1)
            
            data = return_list_expense
            for row, entry_data in enumerate(data, start=3):
                # Alternate text color for each row
                fg_color = "#bebec2" if row % 2 == 0 else "#71ace3"
                
                for col, value in enumerate(entry_data):
                    entry = ctk.CTkLabel(scrollable_frame,
                                            text=value, width=10,
                                            justify='center',
                                            fg_color=fg_color,
                                            corner_radius = 2,
                                            text_color="black")
                    entry.grid(row=row, column=col, sticky="nwes",padx=1)
        else:
            ctk.CTkLabel(scrollable_frame, text= "No Expense today",
                                                justify='center',
                                                fg_color="#0784b5",
                                                corner_radius = 2,
                                                text_color="black").grid(row=1, column=0, columnspan=3)


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
            self.Controller.Create_transfer(from_account, to_account, transfer_date, note, amount,Bank_verified=False)

            
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
        
        def go_back():
            self.todays_expense_screen()
        Go_back_button = ctk.CTkButton(self.control_frame_view, text="Go back", command=go_back)
        Go_back_button.grid(row=12, column=4,columnspan = 4, sticky="we")
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

        categories = self.get_sub_category_list("Income")
        
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
            self.Controller.add_transaction(income_date, note, amount, category, sub_category,False)
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
        def go_back():
            self.todays_expense_screen()
        Go_back_button = ctk.CTkButton(self.control_frame_view, text="Go back", command=go_back)
        Go_back_button.grid(row=16, column=4,columnspan = 4, sticky="we")
        
        
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
        
        categories = self.get_sub_category_list("Expense")
        
        
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
            sub_category = from_dropdown.get()
            if self.fixed_expense == True:
                category = "Fixed Expense"
                self.Controller.add_transaction(expense_date, note, amount, category,sub_category,False)
            else:
                category = "Expense"
                self.Controller.add_transaction(expense_date, note, amount, category,sub_category,False)
                
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
        submit_button.grid(row=16, column=0,columnspan = 4, sticky="we")
        
        def go_back():
            self.todays_expense_screen()
        Go_back_button = ctk.CTkButton(self.control_frame_view, text="Go back", command=go_back)
        Go_back_button.grid(row=16, column=4,columnspan = 4, sticky="we")

    def add_year(self, year):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()

        table_name = f"Budget{year}"
        message = self.Controller.add_year(table_name,year)
        
        ctk.CTkLabel(self.control_frame_view,
                                text = message,
                                text_color="black",
                                fg_color="#39ace7",
                                width=420,height= 30,
                                justify="center",
                                font=("arial", 15)
                                ).grid(row=0, column=0, columnspan=5, rowspan=4, sticky="ew")
        def go_back():
            self.todays_expense_screen()
        Go_back_button = ctk.CTkButton(self.control_frame_view, text="Go back", command=go_back)
        Go_back_button.grid(row=4, column=0,columnspan = 4, sticky="we")
        
    def Add_year_scree(self):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()
        background = "#bebec2" #black
        background2 = "#71ace3" # light blue 
        background3 = "#39ace7" #bright blue 
        background4 = "#0784b5" # dark blue
        text_color = "black"
        header = ctk.CTkLabel(self.control_frame_view,
                                text = "Add more years",
                                text_color=text_color,
                                fg_color=background4,
                                width=420,height= 30,
                                justify="center",
                                font=("arial", 15)
                                )
        header.grid(row=0,column=0,columnspan=2, sticky="ew")
        
        label1 = ctk.CTkLabel(self.control_frame_view,
                                text = "years",
                                text_color=text_color,
                                fg_color=background3,
                                width=20,height= 30,
                                justify="center",
                                font=("arial", 15)
                                )
        label1.grid(row=1,column=0,columnspan=1, sticky="ew")
        
        Entry = ctk.CTkEntry(self.control_frame_view,text_color=text_color)
        Entry.insert(0, "YYYY")  # Set initial text
        Entry.bind("<FocusIn>", lambda event: Entry.delete(0, "end"))  # Remove text on focus
        Entry.grid(row=2, column=0)
        ctk.CTkLabel(self.control_frame_view, text="Current available years",
                            justify='center',
                            fg_color=background3,
                            corner_radius = 2,
                            text_color="black"
                            ).grid(row=1, column=1, sticky="ewns", padx=1)
        width = 200
        scrollable_frame = ctk.CTkScrollableFrame(self.control_frame_view,
                                                    width=130, height= 80,orientation='horizontal')
        scrollable_frame.grid(row=2, column=1, rowspan=2)
        
        years = self.Controller.View_all_year_table()
        
        i = 0
        row = 0
        o = 0
        for i in range(len(years)):
            label = ctk.CTkLabel(scrollable_frame,
                                    text = years[i],
                                    text_color= "black",
                                    fg_color= "white",
                                    width= 30,
                                    )
            label.grid(row=row, column=o, pady = 1, padx = 1)
            row = row + 1 
            if row == 2:
                o = o + 1
                row = 0
                
            
            
        
        def summit():
            year = Entry.get()
            self.add_year(year)
        # Create a submit button
        submit_button = ctk.CTkButton(self.control_frame_view, text="Submit", command=summit)
        submit_button.grid(row=7, column=0, sticky="we")
        
        def go_back():
            self.todays_expense_screen()
        Go_back_button = ctk.CTkButton(self.control_frame_view, text="Go back", command=go_back)
        Go_back_button.grid(row=7, column=1, sticky="we")


    def Scan_statement(self):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()
        
        header = ctk.CTkLabel(self.control_frame_view,
                                text="Drag and Drop Files",
                                text_color="black",
                                bg_color='#0784b5')
        header.pack(fill="x")
        
        #drop_zone = ctk.CTkLabel(self.control_frame_view,
        #                        text="Drop zone",
        #                        text_color="black",
        #                        bg_color='#bebec2',
        #                        height=125)
        #drop_zone.pack(fill="x")

        # Define the drop event handler
        def handle_drop():
            path = filedialog.askopenfilename(initialdir="/Users/kerinpatel/Desktop",title="select a file to process", filetypes= (("pdf files" , "*.PDF"),))
            self.Controller.Process_pdf(path)
            #self.PDF_process_screen(expense_list)
            

        select = ctk.CTkButton(self.control_frame_view,
                                text="Upload",
                                command=handle_drop,
                                text_color="black",
                                fg_color="#71ace3",
                                hover_color='#bebec2',
                                height=125)
        select.pack(fill="both")
                
        def go_back():
            self.todays_expense_screen()

        Go_back_button = ctk.CTkButton(self.control_frame_view, text="Go back", command=go_back, height=50)
        Go_back_button.pack(fill="x")

##Delete Year, Add Starting balance, change database key, Add data base

    def add_data_base(self):
        pass
    
    def change_data_base_key(self):
        pass
    
    
    def Add_starting_balance_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()
            
        background = "#bebec2" #black
        background2 = "#71ace3" # light blue 
        background3 = "#39ace7" #bright blue 
        background4 = "#0784b5" # dark blue
        text_color = "black"
        header = ctk.CTkLabel(self.control_frame_view,
                                text = "Add Starting Balance",
                                text_color=text_color,
                                fg_color=background4,
                                width=420,height= 30,
                                justify="center",
                                font=("arial", 15)
                                )
        header.grid(row=0,column=0,columnspan=2, sticky="ew")
        
        Checking = ctk.CTkLabel(self.control_frame_view,
                                text = "Checking",
                                text_color=text_color,
                                fg_color=background3,
                                width=20,height= 30,
                                justify="center",
                                font=("arial", 15)
                                )
        Checking.grid(row=1,column=0,columnspan=1, sticky="ew")
        checking_entry = ctk.CTkEntry(self.control_frame_view,
                                        text_color= "white",
                                        placeholder_text="00.00",
                                        justify="center",
                                        font=("arial", 15),)
        checking_entry.grid(row=1,column=1,columnspan=1, sticky="ew")
        
        Bail_out = ctk.CTkLabel(self.control_frame_view,
                                text = "Bail out",
                                text_color=text_color,
                                fg_color=background3,
                                width=20,height= 30,
                                justify="center",
                                font=("arial", 15)
                                )
        Bail_out.grid(row=2,column=0,columnspan=1, sticky="ew")
        Bail_out_entry = ctk.CTkEntry(self.control_frame_view,
                                        text_color= "white",
                                        placeholder_text="00.00",
                                        justify="center",
                                        font=("arial", 15),)
        Bail_out_entry.grid(row=2,column=1,columnspan=1, sticky="ew")
        
        Saving = ctk.CTkLabel(self.control_frame_view,
                                text = "Saving",
                                text_color=text_color,
                                fg_color=background3,
                                width=20,height= 30,
                                justify="center",
                                font=("arial", 15)
                                )
        Saving.grid(row=3,column=0,columnspan=1, sticky="ew")
        Saving_entry = ctk.CTkEntry(self.control_frame_view,
                                        text_color= "white",
                                        placeholder_text="00.00",
                                        justify="center",
                                        font=("arial", 15),)
        Saving_entry.grid(row=3,column=1,columnspan=1, sticky="ew")
        
        def summit():
            year = self.current_month_displayed.year
            checking_account = float(checking_entry.get())
            bail_out = float(Bail_out_entry.get())
            savings = float(Saving_entry.get())
            bank = False
            message = self.Controller.add_starting_balance(year, checking_account, bail_out, savings,bank)
            # Show a label over the Submit button
            label = ctk.CTkLabel(self.control_frame_view, text=message, text_color="black")
            label.grid(row=5, column=0)
        
        
        Summit = ctk.CTkButton(self.control_frame_view, text="Summit", command=summit)
        Summit.grid(row=4, column=0, sticky="we")
        
        def go_back():
            self.todays_expense_screen()
        Go_back_button = ctk.CTkButton(self.control_frame_view, text="Go back", command=go_back)
        Go_back_button.grid(row=4, column=1, sticky="we")
        
    def delete_year_screen(self):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()
        background = "#bebec2" #black
        background2 = "#71ace3" # light blue 
        background3 = "#39ace7" #bright blue 
        background4 = "#0784b5" # dark blue
        text_color = "black"
        header = ctk.CTkLabel(self.control_frame_view,
                                text = "Remove years",
                                text_color=text_color,
                                fg_color=background4,
                                width=420,height= 30,
                                justify="center",
                                font=("arial", 15)
                                )
        header.grid(row=0,column=0,columnspan=2, sticky="ew")
        
        label1 = ctk.CTkLabel(self.control_frame_view,
                                text = "years",
                                text_color=text_color,
                                fg_color=background3,
                                width=20,height= 30,
                                justify="center",
                                font=("arial", 15)
                                )
        label1.grid(row=1,column=0,columnspan=1, sticky="ew")
        
        Entry = ctk.CTkEntry(self.control_frame_view,text_color=text_color)
        Entry.insert(0, "YYYY")  # Set initial text
        Entry.bind("<FocusIn>", lambda event: Entry.delete(0, "end"))  # Remove text on focus
        Entry.grid(row=2, column=0)
        ctk.CTkLabel(self.control_frame_view, text="Current available years",
                            justify='center',
                            fg_color=background3,
                            corner_radius = 2,
                            text_color="black"
                            ).grid(row=1, column=1, sticky="ewns", padx=1)
        width = 200
        scrollable_frame = ctk.CTkScrollableFrame(self.control_frame_view,
                                                    width=130, height= 80,orientation='horizontal')
        scrollable_frame.grid(row=2, column=1, rowspan=2)
        
        years = self.Controller.View_all_year_table()
        
        i = 0
        row = 0
        o = 0
        for i in range(len(years)):
            label = ctk.CTkLabel(scrollable_frame,
                                    text = years[i],
                                    text_color= "black",
                                    fg_color= "white",
                                    width= 30,
                                    )
            label.grid(row=row, column=o, pady = 1, padx = 1)
            row = row + 1 
            if row == 2:
                o = o + 1
                row = 0
                
            
            
        
        def summit():
            year = Entry.get()
            self.Delete_year(year)
        # Create a submit button
        submit_button = ctk.CTkButton(self.control_frame_view, text="Submit", command=summit)
        submit_button.grid(row=7, column=0, sticky="we")
        
        def go_back():
            self.todays_expense_screen()
        Go_back_button = ctk.CTkButton(self.control_frame_view, text="Go back", command=go_back)
        Go_back_button.grid(row=7, column=1, sticky="we")

    def Delete_year(self,year):
        # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()
            
        message = self.Controller.delete_year(year)
        
        ctk.CTkLabel(self.control_frame_view,
                                text = message,
                                text_color="black",
                                fg_color="#39ace7",
                                width=420,height= 30,
                                justify="center",
                                font=("arial", 15)
                                ).grid(row=0, column=0, columnspan=5, rowspan=4, sticky="ew")
        def go_back():
            self.todays_expense_screen()
        Go_back_button = ctk.CTkButton(self.control_frame_view, text="Go back", command=go_back)
        Go_back_button.grid(row=4, column=0,columnspan = 4, sticky="we")
        
        
    def refresh_view(self):
        date = datetime.strftime(self.current_month_displayed, "%Y-%m-%d")
        self.custom_month_budget_table_frame(date)
        
    
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
        
        monthly_expenses = math.fsum(float(entry[-1]) for entry in return_list)
        monthly_transfer_In = math.fsum(float(entry[-3]) for entry in return_list)
        monthly_transfer_Out = math.fsum(float(entry[-4]) for entry in return_list)
        monthly_income = math.fsum(float(entry[-2]) for entry in return_list)
        
        
        ctk.CTkLabel(self.monthly_view,bg_color="black").grid(row=0, column=0, columnspan=3, sticky="ewns")
        ctk.CTkLabel(self.monthly_view,bg_color="black").grid(row=1, column=0, columnspan=3, sticky="ewns")
        # Monthly Summary label
        ctk.CTkLabel(self.monthly_view, text="Monthly Summary", text_color=text_color,fg_color=background4, width=420,height= 30, justify="center", font=("arial", 15)).grid(row=0, column=0, columnspan=3, sticky="ew",pady=1)

        ctk.CTkLabel(self.monthly_view, text=f"From - {start_date}\n   To - {end_date}", text_color=text_color, width=width, anchor="e", bg_color=background4,font=("arial", 13)).grid(row=1, column=0, sticky="ew",pady=1)

        ctk.CTkLabel(self.monthly_view, text="Starting Balance", text_color=text_color, width=width,height=30, font=("arial", 10), anchor="e", bg_color=background4).grid(row=1, column=1, sticky="ew",pady=1)
        ctk.CTkLabel(self.monthly_view, text="Ending Balance", text_color=text_color, width=width,height=30, font=("arial", 10), bg_color=background4).grid(row=1, column=2, sticky="ew",pady=1)



        # Account labels
        accounts = ["Checking", "Bail out", "Savings","-------------","Monthly Income","Monthly Expense","Monthly transfer In","Monthly transfer Out"]
        for idx, account in enumerate(accounts, start=2):
            ctk.CTkLabel(self.monthly_view, text=account,bg_color=background2, text_color=text_color, width=width,height=height, justify="center", anchor="center").grid(row=idx, column=0, sticky="ew")

        # Starting balances
        starting_balances = [start_checking, start_bailout, start_saving,"",monthly_income,monthly_expenses,monthly_transfer_In,monthly_transfer_Out]
        for idx, balance in enumerate(starting_balances, start=2):
            # Alternate text color for each row
            if balance == "":
                ctk.CTkLabel(self.monthly_view, text=f"{balance}", text_color=text_color, width=width,height=height, justify="center",anchor=side).grid(row=idx, column=1, sticky="ew",padx="10")
            else:
                ctk.CTkLabel(self.monthly_view, text=f"$ {balance}", text_color=text_color, width=width,height=height, justify="center",anchor=side).grid(row=idx, column=1, sticky="ew",padx="10")

        # Ending balances
        ending_balances = [end_checking, end_bailout, end_saving]
        for idx, balance in enumerate(ending_balances, start=2):
            ctk.CTkLabel(self.monthly_view, text=f"$ {balance}", text_color=text_color, width=width,height=height, justify="center").grid(row=idx, column=2, sticky="ew",padx="10")
        
        self.activity_view(start_date)
        
    def view_expense(self, start_date, subcategory):
        return_list_expense = self.Controller.look_up_expense(start_date, subcategory)
        self.view_expense_list(return_list_expense)
        

    def activity_view(self, start_date):
        
        # Clear existing content of control_frame_view
        for widget in self.Activity_frame.winfo_children():
            widget.destroy()
        frame = ctk.CTkScrollableFrame(self.Activity_frame,
                                        height=40
                                        )
        frame.pack(expand=True,fill="both")

        sub_catogeiors = self.get_sub_category_list("all")
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
            self.view_expense(start_date, subcategory)
        y_offset = 0  # Initial y-coordinate offset
        
        summary_list = self.Controller.view_sub_category_summary(start_date)
        
        if sub_catogeiors == None:
            inner_frame = ctk.CTkFrame(frame)
            inner_frame.pack(fill="x")  # Use pack to manage inner_frame
            label_1 = ctk.CTkLabel(inner_frame,
                                    text=f"No Transactions available",
                                    width=100,
                                    bg_color=background4,
                                    text_color=text_Color,
                                    corner_radius=2,wraplength=100)
            label_1.pack( fill = "both")  # Use pack to manage label_1
        elif sub_catogeiors != None:
            for i in range(len(summary_list)):
                subcategory = summary_list[i][0]
                total_amount = summary_list[i][1]
                
                inner_frame = ctk.CTkFrame(frame)
                inner_frame.pack(fill="x")  # Use pack to manage inner_frame
                label_1 = ctk.CTkLabel(inner_frame,
                                        text=f"{subcategory}",
                                        width=100,
                                        bg_color=background4,
                                        text_color=text_Color,
                                        corner_radius=2,wraplength=100)
                label_1.pack(side="left")  # Use pack to manage label_1

                label_2 = ctk.CTkLabel(inner_frame,
                                        text=f"Amount - ${total_amount}\t",
                                        width=180,
                                        bg_color=background,
                                        fg_color=background,
                                        anchor="e",
                                        text_color=text_Color,
                                        corner_radius=2)
                label_2.pack(side="left")  # Use pack to manage label_2

                view_button = ctk.CTkButton(inner_frame, text="View Transactions", bg_color=background3,
                                            fg_color=background2,
                                            text_color=text_Color,
                                            hover_color=hover_color,
                                            border_width=border_Width,
                                            border_color=border_Color,
                                            corner_radius=5,
                                            command=lambda subcategory=subcategory: summit(subcategory)
                                            )
                view_button.pack(side="left")  # Use pack to manage view_button


                y_offset += 30  # Increase the y-coordinate offset for the next widget


        
Driver('Budget app', '1200X1200').mainloop()


#source env/bin/activate
