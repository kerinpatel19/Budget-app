    # Clear existing content of control_frame_view
        for widget in self.control_frame_view.winfo_children():
            widget.destroy()
        
        header = ctk.CTkLabel(self.control_frame_view,
                                text="Drag and Drop Files",
                                text_color="black",
                                bg_color='#0784b5')
        header.pack(fill="x")
        
        drop_zone = ctk.CTkLabel(self.control_frame_view,
                                text="Drop zone",
                                text_color="black",
                                bg_color='#bebec2',
                                height=125)
        drop_zone.pack(fill="x")

        # Define the drop event handler
        def handle_drop(event):
            files = event.data
            for file_path in files:
                print(f"Dropped file: {file_path}")

        # Bind the drop event to the drop_zone label
        drop_zone.bind("<Drop>", handle_drop)
        drop_zone.drop_target_register(ctk.DND_FILES)
        drop_zone.dnd_bind('<<Drop>>', handle_drop)

        def go_back():
            self.todays_expense_screen()

        Go_back_button = ctk.CTkButton(self.control_frame_view, text="Go back", command=go_back)
        Go_back_button.pack(fill="x")