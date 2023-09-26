from tkinter import *

root = Tk()

root.geometry("300x300")

buttonquit = Button(root, text="Exit", command=root.quit)
buttonquit.grid(row=1,column=0)

questionlabel=Label(root, text="Which icons belong together?")
questionlabel.grid(row=0,column=0)

my_canvas=Canvas(root,width=200,height=200, bg="white")
my_canvas.grid(row=3,column=0)

my_canvas.create_oval(10, 190, 40, 160, fill="red")
my_canvas.create_rectangle(30,30,60,60, fill="red")

my_canvas.create_oval(50, 190, 90, 150, fill="green")
my_canvas.create_rectangle(150,30,100,80, fill="green")

my_canvas.create_oval(20, 100, 70, 150, fill="yellow")
my_canvas.create_rectangle(160,140,190,110, fill="yellow")






root.mainloop()