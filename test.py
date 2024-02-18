import tkinter as tk
from tkinter import ttk
class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        ttk.Label(self,background="#8e9bb9").pack(expand= True, fill='both')
  