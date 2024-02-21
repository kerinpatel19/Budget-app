from tkinter import *

window = Tk() 

window.geometry('500x250') # size of the screen
window.title("Budget App")

window.config(background="#ffffff")


def main():
    frame = Frame(window, width=500,height=250,bg='yellow')
    frame.place(x=0,y=0)
    
    btn1 = Button(frame,text='Home',command=main)
    btn1.place(x=10,y=10)
    btn2 = Button(frame,text='Screen 1',command=screen_1)
    btn2.place(x=10,y=50)
    btn3 = Button(frame,text='Screen 2',command=screen_2)
    btn3.place(x=10,y=80)

def screen_1():
    frame1 = Frame(window, width=500,height=250,bg='green')
    frame1.place(x=0,y=0)
    
    btn1 = Button(frame1,text='Home',command=main)
    btn1.place(x=10,y=10)
    btn2 = Button(frame1,text='Screen 1',command=screen_1)
    btn2.place(x=10,y=50)
    btn3 = Button(frame1,text='Screen 2',command=screen_2)
    btn3.place(x=10,y=80)
    
def screen_2():
    frame2 = Frame(window, width=500,height=250,bg='blue')
    frame2.place(x=0,y=0)
    
    btn1 = Button(frame2,text='Home',command=main)
    btn1.place(x=10,y=10)
    btn2 = Button(frame2,text='Screen 1',command=screen_1)
    btn2.place(x=10,y=50)
    btn3 = Button(frame2,text='Screen 2',command=screen_2)
    btn3.place(x=10,y=80)
    
main()
window.mainloop()
#source venv/bin/activate
