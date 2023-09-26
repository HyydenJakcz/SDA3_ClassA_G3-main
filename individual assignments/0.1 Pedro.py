from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import Canvas
import tkinter

#create window
root = tk.Tk()
root.title('Tkinter Demo')


#set window size
window_width = 800
window_height = 500

#prevent the window from being resizeable
root.resizable(False, False)

#In order to center the window in your screen:
#get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#find the center point
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)

#set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


#root.iconbitmap('C:/Users/murde/Mechatronics/Software Design & Architecture/assets/shapes.ico')

ttk.Label(root, text='What are those???', font="Cambria").pack()

frame = Frame(root)
frame.pack()

#Create canvas
canvas_width = 750
canvas_height = 400
c = Canvas(root, height=canvas_height, width=canvas_width, bg="white")
#shape = createfunction(starting_point_x, starting_point_y, ending_point_x, ending_point_y, fill="color")
bc = c.create_oval(0, 0, canvas_width/3, canvas_height/2, fill="blue")  #Blue Circle
yc = c.create_oval(canvas_width/3, 0, 2*canvas_width/3, canvas_height/2, fill="yellow")  #Yellow Circle
rc = c.create_oval(2*canvas_width/3, 0, canvas_width, canvas_height/2, fill="red")  #Red Circle
rs = c.create_rectangle(0, canvas_height/2, canvas_width/3, canvas_height, fill="red")  #Red Square
bs = c.create_rectangle(canvas_width/3, canvas_height/2, 2*canvas_width/3, canvas_height, fill="blue")  #Blue Square
ys = c.create_rectangle(2*canvas_width/3, canvas_height/2, canvas_width, canvas_height, fill="yellow")  #Yellow Square
c.pack()


bottomframe = Frame(root)
bottomframe.pack(side = BOTTOM)

#Creates an Exit button with a command "destroy root window"
exitbutton = Button(bottomframe, text="Exit", fg="black", height=50, width=20, background="white", command=root.destroy)
exitbutton.pack(side = BOTTOM)


root.mainloop()