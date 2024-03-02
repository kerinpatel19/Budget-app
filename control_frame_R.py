import customtkinter as ctk
from controller import Controller

class Control_frame_R(ctk.CTkFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        from budget_frame_L import Budget_frame_L
        self.Controller = Controller()
        self.budget_frame = Budget_frame_L(self)
        self.accounts = ["Checking", "Bail out", "saving"]
        self.Create_all_frames()
        self.create_control_buttons_frame()
        
    def Create_all_frames(self):
        self.control_frame = ctk.CTkFrame(self,border_width = 1, border_color="Black")
        self.control_frame.grid(row=0, column=0, sticky="nsew")
        self.control_frame_view = ctk.CTkFrame(self, border_width = 1, border_color="Black")
        self.control_frame_view.grid(row=1, column=0, sticky="nsew")
        self.monthly_view = ctk.CTkLabel(self, text="Monthly view")
        self.monthly_view.grid(row=2, column=0, sticky="nsew") 
        
        
    def create_control_buttons_frame(self):
        
        background = "green"
        text_Color = "white"
        border_Width = 2
        border_Color = "black"

        ctk.CTkButton(self.control_frame, text="Transfer", width=5,command= self.create_transfer_screen, border_width = border_Width, border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=0, column=0, columnspan=1, rowspan=1, sticky="ew")
        ctk.CTkButton(self.control_frame, text="Add Income", width=5,border_width = border_Width, border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=0, column=1, columnspan=1, rowspan=1, sticky="ew")
        ctk.CTkButton(self.control_frame, text="Expense", width=5,border_width = border_Width, border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=0, column=2, columnspan=1, rowspan=1, sticky="ew")
        ctk.CTkButton(self.control_frame, text="Edit Expense", width=5,border_width = border_Width, border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=0, column=3, columnspan=1, rowspan=1, sticky="ew")
        
        ctk.CTkButton(self.control_frame, text="last month",border_width = border_Width, border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=1, column=0, columnspan=1, rowspan=1, sticky="wen")
        ctk.CTkButton(self.control_frame, text="Current month",border_width = border_Width, border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=1, column=1, columnspan=2, rowspan=1, sticky="ew")
        ctk.CTkButton(self.control_frame, text="Next month",border_width = border_Width, border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=1,column=3, columnspan=1, rowspan=1, sticky="wen")
  
        ctk.CTkButton(self.control_frame, text="scan statement",border_width = border_Width, border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=2, column=0, columnspan=1, rowspan=1, sticky="ewn")
        ctk.CTkButton(self.control_frame, text="Add more year",border_width = border_Width, border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=2, column=1, columnspan=1, rowspan=1, sticky="ew")
        ctk.CTkButton(self.control_frame, text="Add Category",border_width = border_Width, border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=2,column=2, columnspan=1, rowspan=1, sticky="ewn")
        ctk.CTkButton(self.control_frame, text="More",border_width = border_Width, border_color=border_Color,text_color=text_Color,fg_color=background).grid(row=2,column=3, columnspan=1, rowspan=1, sticky="ewn")
  
    
    def get_sub_category_list(self):
        return_list = self.Controller.sub_category()
        return return_list
    #row 2   frame 2  
    def default_input_area_screen(self):  # Align to bottom with padding
        ctk.CTkLabel(self.control_frame_view, text="Text", width=20).grid(row=1, column=0, sticky="n")

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

        ctk.CTkLabel(self.control_frame_view, text="From Account:").grid(row=0, column=0)
        combo_a = ctk.CTkComboBox(self.control_frame_view, values=self.accounts)
        combo_a.grid(row=0, column=1)
        combo_a.bind("<<ComboboxSelected>>", update_to_options)


        ctk.CTkLabel(self.control_frame_view, text="To Account:").grid(row=1, column=0)
        combo_b = ctk.CTkComboBox(self.control_frame_view, values=self.accounts)
        combo_b.grid(row=1, column=1)
        combo_b.bind("<<ComboboxSelected>>", update_to_options)



        ctk.CTkLabel(self.control_frame_view, text="Date: ").grid(row=2, column=0)
        transfer_date_entry = ctk.CTkEntry(self.control_frame_view)
        transfer_date_entry.insert(0, "YYYY-MM-DD")  # Set initial text
        transfer_date_entry.bind("<FocusIn>", lambda event: transfer_date_entry.delete(0, "end"))  # Remove text on focus
        transfer_date_entry.grid(row=2, column=1)

        ctk.CTkLabel(self.control_frame_view, text="Note:").grid(row=3, column=0)
        note_entry = ctk.CTkEntry(self.control_frame_view)
        note_entry.insert(0, "ABC...")  # Set initial text
        note_entry.bind("<FocusIn>", lambda event: note_entry.delete(0, "end"))  # Remove text on key release
        note_entry.grid(row=3, column=1)

        ctk.CTkLabel(self.control_frame_view, text="Amount:").grid(row=4, column=0)
        amount_entry = ctk.CTkEntry(self.control_frame_view)
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
            submit_label = ctk.CTkLabel(self.control_frame_view, text="Transfer submitted successfully!")
            submit_label.grid(row=5, column=1)

            self.budget_frame.custom_month_budget_table_frame(transfer_date)

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
        submit_button = ctk.CTkButton(self.control_frame_view, text="Submit", command=submit_transfer)
        submit_button.grid(row=5)



    def monthly_overview(self, return_list):

        start_date = return_list[0][0]
        end_date = return_list[-1][0]
        
        start_checking = return_list[0][1]
        end_checking = return_list[-1][1]
        
        start_bailout = return_list[0][2]
        end_bailout = return_list[-1][2]
        
        start_saving = return_list[0][3]
        end_saving = return_list[-1][3]
        
    
        
        ctk.CTkLabel(self.monthly_view, text=start_date).grid(row=0, column=0)
        ctk.CTkLabel(self.monthly_view, text=end_date).grid(row=0, column=3)
        # Align to bottom with padding
        ctk.CTkLabel(self.monthly_view, text="Accounts").grid(row=1, column=0,)
        ctk.CTkLabel(self.monthly_view, text="Starting Bal").grid(row=1, column=1,)
        ctk.CTkLabel(self.monthly_view, text="Ending Bal").grid(row=1, column=3,)
        
        ctk.CTkLabel(self.monthly_view, text="Checking").grid(row=2, column=0,)
        ctk.CTkLabel(self.monthly_view, text=start_checking).grid(row=2, column=1,)
        ctk.CTkLabel(self.monthly_view, text=end_checking).grid(row=2, column=3,)
        
        ctk.CTkLabel(self.monthly_view, text="Bail out").grid(row=3, column=0,)
        ctk.CTkLabel(self.monthly_view, text=start_bailout).grid(row=3, column=1,)
        ctk.CTkLabel(self.monthly_view, text=end_bailout).grid(row=3, column=3,)
        
        ctk.CTkLabel(self.monthly_view, text="Savings").grid(row=4, column=0,)
        ctk.CTkLabel(self.monthly_view, text=start_saving).grid(row=4, column=1,)
        ctk.CTkLabel(self.monthly_view, text=end_saving).grid(row=4, column=3,)
        

        
        
        #self.control_frame_view = tk.LabelFrame(self.frame2_control, text="Input area")
        #self.control_frame_view.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)  # Align to bottom with padding
        #tk.Label(self.control_frame_view, text="Text", width=20, padding=10).grid(row=1, column=0, rowspan=4, sticky="n")
