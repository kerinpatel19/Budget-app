from tkinter import *

class screen_num_3:
    
    def __init__(self, master):
        
        frame = Frame(master, width=500,height=250,bg='yellow')
        frame.place(x=0,y=0)
        
        btn1 = Button(frame,text='Home',command=test.main)
        btn1.place(x=10,y=10)
        btn2 = Button(frame,text='Screen 1',command=test.screen_1)
        btn2.place(x=10,y=50)
        btn3 = Button(frame,text='Screen 2',command=test.screen_2)
        btn3.place(x=10,y=80)