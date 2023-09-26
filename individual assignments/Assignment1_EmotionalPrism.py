import asyncio
import time
from tkinter import *
import tkinter as tk
from turtle import width

#create window
root = tk.Tk()
root.title('Emotional Prism')

#set window size
window_width = 600
window_height = 600

#set placement of the eye
start_Eye_Position_x = 300
start_Eye_Position_y = 190

#define the parameters for the eye 
eye_radius = 75
line_Length = 50
line_min_movement = 2
Refresh_Sec = 0.01


#define parent class
class Robot:
    
    async def eye_movement(self, window, canvas, xinc, yinc):
        #insert eye movement here
        eye = canvas.create_line(start_Eye_Position_x-eye_radius, start_Eye_Position_y, start_Eye_Position_x-eye_radius, start_Eye_Position_y+line_Length, width= 6, fill= 'red', tag= 'eye')

        #create the eyelid/eyebox
        canvas.create_rectangle(215,190,380,240, outline = 'black', width = 5, tag = 'eyelid')
        canvas.pack()
        canvas.tag_raise('eyelid','eye') #make sure the eyelid is drawn on top of the eye

        while True:
            canvas.move(eye,xinc,yinc)
            window.update()
            time.sleep(Refresh_Sec)
            line_pos = canvas.coords(eye)
            # unpack array to variables
            tx,ty,bx,by = line_pos
            if tx < start_Eye_Position_x-eye_radius or tx > start_Eye_Position_x+eye_radius:
                xinc = -xinc


#define child classes
class Chill(Robot):
    def __init__(self, bg_color):
        self.bg_color=bg_color
        

    def smoke_joint(self):
        #delete previous attributes
        c.delete("tearoval", "tearpolygon", "eyebrow1", "eyebrow2","eyebrow3","eyebrow4","sweat","eyebrow5","eyebrow6")
        #add junko
        c.create_polygon(395,390,495,400,495,370,395,380, fill='peru', outline='peachpuff', tags='junkopolygon')


class Sad(Robot):
    def __init__(self, bg_color):
        self.bg_color=bg_color
        
        
    def crying(self):
        #delete previous attributes
        c.delete("eyebrow1", "eyebrow2","eyebrow3","eyebrow4","sweat","junkopolygon")
        #create tear for sad emotion
        c.create_oval(340,290,390,340, fill="blue", tags='tearoval')
        c.create_polygon(340,310,390,310,365,250, fill="blue", tags='tearpolygon')
        c.create_line(canvas_width/2-60,180, canvas_width/2-20,140, width=6, tags="eyebrow5")
        c.create_line(canvas_width/2+20,140, canvas_width/2+60,180, width=6, tags= "eyebrow6")


class Rage(Robot):
    def __init__(self, bg_color):
        self.bg_color=bg_color

    def Look_mean(self):
        #delete previous attributes
        c.delete("tearoval", "tearpolygon","eyebrow3","eyebrow4","sweat","eyebrow5","eyebrow6","junkopolygon")
        #look mean eyebrows
        c.create_line(canvas_width/2-60,140, canvas_width/2-20,180, width=6, tags="eyebrow1")
        c.create_line(canvas_width/2+20,180, canvas_width/2+60,140, width=6, tags= "eyebrow2")


class Nervous(Robot):
    def __init__(self, bg_color):
        self.bg_color=bg_color

    def be_nervous(self):
        #delete previous attributes
        c.delete("tearoval", "tearpolygon", "eyebrow1", "eyebrow2","eyebrow5","eyebrow6")
        #nervousnes here
        c.create_arc(170,200,190,250,start=180, extent=180,outline="blue",width=5,style=tk.ARC,tags="sweat")
        c.create_line(canvas_width/2-60,180, canvas_width/2-20,140, width=6, tags="eyebrow3")
        c.create_line(canvas_width/2+20,140, canvas_width/2+60,180, width=6, tags= "eyebrow4")
        print("Brrrrrrrrr shakie shakie bing chilling bitch!")
        


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

#function for changing the canvas background color
def changeColor(color): #pass a string
    c.configure(bg=color)

#Create canvas
canvas_width = window_width
canvas_height = window_height
c = Canvas(root, height=canvas_height, width=canvas_width, bg='white')
#shape = createfunction(starting_point_x, starting_point_y, ending_point_x, ending_point_y, fill="color")
robot_body=c.create_oval(canvas_width/5, canvas_height/5, 4*canvas_width/5, 4*canvas_height/5, fill="grey")

#shape= createfunction(starting_point_x, starting_point_y, first_curve_x, first_curve_y, second_curve_x, second_curve_y, ending_point_x, ending_point_y, smoothness, widthness)
antenna=c.create_line(canvas_width/2, canvas_height/5, (canvas_width/2)+30, (canvas_height/5)-30, (canvas_width/2)+120, (canvas_height/5)-30, 3*canvas_width/4, canvas_height/10, smooth=1, width=5)
antenna_ball=c.create_oval((3*canvas_width/4)-25, (canvas_height/10)-25, (3*canvas_width/4)+25, (canvas_height/10)+25, fill="red")
mouth=c.create_rectangle(canvas_width/2-100, canvas_height/2+50, canvas_width/2+100, canvas_height/2+110, fill="cyan")
mouthline_horizontal1=c.create_line(canvas_width/2-100, canvas_height/2+70, canvas_width/2+100, canvas_height/2+70)
mouthline_horizontal2=c.create_line(canvas_width/2-100, canvas_height/2+90, canvas_width/2+100, canvas_height/2+90)
mouthline_vertical1=c.create_line(canvas_width/2-60, canvas_height/2+50, canvas_width/2-60, canvas_height/2+110)
mouthline_vertical2=c.create_line(canvas_width/2-20, canvas_height/2+50, canvas_width/2-20, canvas_height/2+110)
mouthline_vertical3=c.create_line(canvas_width/2+20, canvas_height/2+50, canvas_width/2+20, canvas_height/2+110)
mouthline_vertical4=c.create_line(canvas_width/2+60, canvas_height/2+50, canvas_width/2+60, canvas_height/2+110)
c.pack()

#create objects
normalrobot=Robot()
chillrobot=Chill("cyan")
sadrobot=Sad("magenta")
ragerobot=Rage("red")
nervousrobot=Nervous("yellow")


#Create buttons
chillbutton = Button(c, text="Chill", fg="black", height=2, width=12, background="white", command=lambda:[changeColor(chillrobot.bg_color),chillrobot.smoke_joint()])
chillbutton.place(x=10, y=10)

sadbutton = Button(c, text="Sad", fg="black", height=2, width=12, background="white", command=lambda:[changeColor(sadrobot.bg_color),sadrobot.crying()])
sadbutton.place(x=10, y=60)

ragebutton = Button(c, text="Rage", fg="black", height=2, width=12, background="white", command=lambda:[changeColor(ragerobot.bg_color),ragerobot.Look_mean()])
ragebutton.place(x=10, y=110)#+50px

nervousbutton = Button(c, text="Nervous", fg="black", height=2, width=12, background="white", command=lambda:[changeColor(nervousrobot.bg_color),nervousrobot.be_nervous()])
nervousbutton.place(x=10, y=160)#+50px

#Creates an Exit button with a command "destroy root window"
exitbutton = Button(c, text="Exit", fg="black", height=2, width=12, background="white", command=root.destroy)
exitbutton.place(x=10, y=canvas_height-100)

#eye movement
loop=asyncio.get_event_loop()
loop.run_until_complete(normalrobot.eye_movement(root, c, line_min_movement, 0))

root.mainloop()