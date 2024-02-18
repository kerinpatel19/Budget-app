import tkinter as tk
from tkinter import ttk
from test import Menu
class App(tk.Tk):
    def __init__(self, title, size):
        
        #main setup of the app
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        
        #widgets
        self.menu = Menu(self)
        
        
        
        
        #run 
        self.mainloop()
        
        
App('Budget app',(600,600))

#source venv/bin/activate