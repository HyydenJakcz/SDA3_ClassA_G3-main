from random import shuffle
from tkinter.simpledialog import askstring
import cv2
import time
import imutils
import numpy as np
import tkinter as tk
from tkinter import font
from transitions import Machine
from serial.tools import list_ports
from DoBotArm import DoBotArm as Dbt

#lists containing Piece objects
bluePieceList=[]
yellowPieceList=[]
greenPieceList=[]
allPieceList=[]

#dimensions of pick up field
boxHeight = 140+30
boxLength = 120+19

#dimensions of cropped image
imageHeight = 215
imageLength = 185

#create a connection to the robot
def port_selection():
    # Choosing port
    available_ports = list_ports.comports()
    print('Available COM-ports:')
    for i, port in enumerate(available_ports):
        print(f"  {i}: {port.description}")
    choice = int(input('Choose port by typing a number followed by [Enter]: '))
    return available_ports[choice].device
#create SystemState class
class SystemState:
    
    #refer to state diagram
    states= ['robot_at_home', 'piece_picked_up', 'robot_moved', 'piece_dropped','piece_instances_created']
    def __init__(self):
        self.machine = Machine(model=self, states=SystemState.states, initial='robot_at_home')
        self.machine.add_transition(trigger='startbutton_pressed',source='robot_at_home',dest='piece_instances_created',
                                    before='create_piece_instances')
        self.machine.add_transition(trigger='pieces_found',source='piece_instances_created',dest='piece_picked_up',
                                    before='pickup')
        self.machine.add_transition(trigger='no_pieces_found',source='piece_instances_created',dest='robot_at_home',
                                    before='no_pieces') #If no pieces are detected, go back to the start state
        self.machine.add_transition(trigger='move_robot',source='piece_picked_up',dest='robot_moved',
                                    before='move')
        self.machine.add_transition(trigger='drop_piece',source='robot_moved',dest='piece_dropped',
                                    before='drop')
        self.machine.add_transition(trigger='move_home',source='piece_dropped',dest='robot_at_home',
                                    before='move_to_home')
        self.machine.add_transition(trigger='not_all_pieces_dropped',source='robot_at_home',dest='piece_picked_up',
                                    before='pickup')
        
    def create_piece_instances(self):
        print("pieces created")
        myCamera.create_piece_instances()

    def pickup(self, position= (60, 60)):
        print("piece picked up")
        myRobot.pickup(position)
        
    def move(self):
        print("robot moved")
        myRobot.move()

    def drop(self):
        print("piece dropped")   
        myRobot.drop()
        time.sleep(1)
        myRobot.move_conveyor_backward(20)

    def move_to_home(self):
        print("at home")
        myRobot.move_to_home()
        
    def no_pieces(self):
        print("I'm so sad cus there's no pieces on the square")

#define Piece class
class Piece:
    def __init__(self, shape, color, position):
        self.shape = shape
        self.color = color
        self.position = position
#define Camera class
class Camera:
    def __init__(self,resolution):
        #resolution is not used as of now
        self.resolution = resolution

    def create_piece_instances(self):
        #open and close camera to only use one frame
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) #Careful here! the first paramater chooses which camera to use
        _,frame = cap.read()
        cap.release()

        #create area threshold to not detect small objects
        mask_area_thres = 100
        #crop frame to only see pickup field
        Cropped_frame=frame[180:395,270:455]
        #Makes the cropped mask x times bigger
        scale_factor=1
        scaled_frame = cv2.resize(Cropped_frame, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
        #convert frame to HSV picture
        hsv = cv2.cvtColor(scaled_frame, cv2.COLOR_BGR2HSV)
        #create threshold for every color
        low_yellow = np.array([25, 70, 120])
        up_yellow = np.array([30, 255, 255])
        low_green = np.array([40, 70, 80])
        up_green = np.array([70, 255, 255])
        low_blue = np.array([90, 60, 70])
        up_blue = np.array([140, 255, 255])
        #create masks for every color
        bmask = cv2.inRange(hsv, low_blue, up_blue)
        gmask = cv2.inRange(hsv, low_green, up_green)
        ymask = cv2.inRange(hsv, low_yellow, up_yellow)
        #find contours according to color masks
        contours_b = cv2.findContours(bmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_b =imutils.grab_contours(contours_b)
        contours_g = cv2.findContours(gmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_g =imutils.grab_contours(contours_g)
        contours_y = cv2.findContours(ymask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_y =imutils.grab_contours(contours_y)
        index= 0
        for c in contours_b:
            #get area of contour
            area_b = cv2.contourArea(c)
            #if area is bigger than threshold: draw contours, get centerpoint, append to object list
            if area_b >mask_area_thres:
                cv2.drawContours(scaled_frame, [c], -1, (255,255,255), 1)
                M = cv2.moments(c)
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])

                bluePieceList.append(Piece("square","blue",[cx,cy]))
                allPieceList.append(Piece("square","blue",[cx,cy]))

                print("Blue piece detected")

                #print("blue")
                #print(cx)
                #print(cy)
                cv2.circle(scaled_frame, (cx, cy), 3, (255,255,255), -1)
                cv2.putText(scaled_frame, "Blue," + str(index), (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
                index+= 1                
        for c in contours_g:
            area_g = cv2.contourArea(c)
            if area_g >mask_area_thres:
                
                cv2.drawContours(scaled_frame, [c], -1, (255,255,255), 1)
                M = cv2.moments(c)
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])
                greenPieceList.append(Piece("square","green",[cx,cy]))
                allPieceList.append(Piece("square", "blue", [cx,cy]))
                #print("green")
                #print(cx)
                #print(cy)
                cv2.circle(scaled_frame, (cx, cy), 3, (255,255,255), -1)
                cv2.putText(scaled_frame, "Green," + str(index), (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
                index+= 1
        for c in contours_y:
            area_y = cv2.contourArea(c)
            if area_y >mask_area_thres:
                
                cv2.drawContours(scaled_frame, [c], -1, (255,255,255), 1)
                M = cv2.moments(c)
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])
                yellowPieceList.append(Piece("square","yellow",[cx,cy]))
                allPieceList.append(Piece("square", "blue", [cx,cy]))
                #print("yellow")
                #print(cx)
                #print(cy)
                cv2.circle(scaled_frame, (cx, cy), 3, (255,255,255), -1)
                cv2.putText(scaled_frame, "Yellow," + str(index), (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
                index+= 1
        winname = "camera"
        cv2.namedWindow(winname)
        cv2.moveWindow(winname, 10, 10)
        cv2.imshow(winname, scaled_frame)
        #image = Image.fromarray(scaled_frame)   #convert to PIL format
        #image = PhotoImage(scaled_frame)        #convert to ImageTk format
        #Canvas.create_image(0, 0, anchor= tk.W, image= image)

#define Robot class
class Robot():

    dropX, dropY, dropZ = 200, 0, 50

    #initialize and home the robot
    def __init__(self):
        #preprogrammed sequence
        #robot homes to the top-right position in real
        #robot homes to the top-left position in the image
        homeX, homeY, homeZ = 280, -120, 50
        port = port_selection()
        print("Connecting")
        print("Homing")
        self.ctrlBot = Dbt.DoBotArm(port, homeX, homeY, homeZ, home = True, homingWait= False)
        self.ctrlBot.commandDelay()

    def pickup(self, position):
        print("I'm picking up so hard right now!")
        #put X in the Y position and vice versa
        rotationMatrix = np.array(((0, -1), 
                              (1, 0)))
        result = np.dot(position, rotationMatrix)
        pointX, pointY = result

        #scale the movement according to the difference in size of points in real and the image
        moveX = boxLength*pointX/imageLength
        moveY = boxHeight*pointY/imageHeight
        self.ctrlBot.moveArmRelXY(-moveX, moveY, jump= True)
        print("wait 1s")
        time.sleep(1)
        #move the arm downwards to pick
        self.ctrlBot.moveArmRelXYZ(0, 0, -80)
        self.ctrlBot.toggleSuction()
        self.ctrlBot.moveArmRelXYZ(0, 0, -20)
        self.ctrlBot.commandDelay()

    def move(self):
        print("I'm moving so hard right now!")        
        self.ctrlBot.moveArmRelXYZ(0, 0, 100, wait= True)
        self.ctrlBot.moveArmXYZ(self.dropX, self.dropY, self.dropZ, jump= True)
        #wait for all the commands to be finished
        self.ctrlBot.commandDelay()

    def drop(self):
        print("I'm dropping so hard right now!")
        self.ctrlBot.toggleSuction()   
        self.ctrlBot.commandDelay()          
                
    def move_to_home(self):
        print("I'm moving to my home so hard right now!")
        self.ctrlBot.moveHome()        
        #wait for all the commands to be finished
        self.ctrlBot.commandDelay()

    def move_conveyor_forward(self, duration = 150):
        print("conveyor go brrrrrr")
        for i in range(duration):
            self.ctrlBot.SetConveyor(enabled= True, speed= 20000)
        self.ctrlBot.SetConveyor(False)
        #wait for all the commands to be finished
        self.ctrlBot.commandDelay()

    def move_conveyor_backward(self, duration = 150):
        print("brrrrrr go conveyor")
        for i in range(duration):
            self.ctrlBot.SetConveyor(enabled= True, speed = -20000)
        self.ctrlBot.SetConveyor(False)
        #wait for all the commands to be finished
        self.ctrlBot.commandDelay()

    def disconnect(self):
        print("Oh God I'm disconnected from my body")
        self.ctrlBot.dobotDisconnect()

def start():
    def main():          
        window.destroy()
        if bluePieceList:
            mySystemState.pieces_found(bluePieceList[0].position)
            print(mySystemState.state)
            mySystemState.move_robot()
            print(mySystemState.state)
            mySystemState.drop_piece()
            print(mySystemState.state)
            mySystemState.move_home()
            print(mySystemState.state)
            bluePieceList.pop(0)            
        elif greenPieceList:
            mySystemState.pieces_found(greenPieceList[0].position)
            print(mySystemState.state)
            mySystemState.move_robot()
            print(mySystemState.state)
            mySystemState.drop_piece()
            print(mySystemState.state)
            mySystemState.move_home()
            print(mySystemState.state)
            greenPieceList.pop(0)            
        elif yellowPieceList:
            mySystemState.pieces_found(yellowPieceList[0].position)
            print(mySystemState.state)
            mySystemState.move_robot()
            print(mySystemState.state)
            mySystemState.drop_piece()
            print(mySystemState.state)
            mySystemState.move_home()
            print(mySystemState.state)
            bluePieceList.pop(0)                
        #print("DEBUGTEST2")
            
        for piece in bluePieceList:
            print("DEBUGTEST4")
            print(piece.position)
            print(piece.shape)
            print(piece.color)
            mySystemState.not_all_pieces_dropped(piece.position)
            print(mySystemState.state)
            mySystemState.move_robot()
            print(mySystemState.state)
            mySystemState.drop_piece()
            print(mySystemState.state)
            mySystemState.move_home()
            print(mySystemState.state)
        
        for piece in greenPieceList:
            print(piece.position)
            print(piece.shape)
            print(piece.color)
            mySystemState.not_all_pieces_dropped(piece.position)
            print(mySystemState.state)
            mySystemState.move_robot()
            print(mySystemState.state)
            mySystemState.drop_piece()
            print(mySystemState.state)
            mySystemState.move_home()
            print(mySystemState.state)

        for piece in yellowPieceList:
            print("DEBUGTEST5")
            print(piece.position)
            print(piece.shape)
            print(piece.color)
            mySystemState.not_all_pieces_dropped(piece.position)
            print(mySystemState.state)
            mySystemState.move_robot()
            print(mySystemState.state)
            mySystemState.drop_piece()
            print(mySystemState.state)
            mySystemState.move_home()
            print(mySystemState.state)
            
        print("All pieces moved")
        bluePieceList.clear()
        greenPieceList.clear()
        yellowPieceList.clear()
        allPieceList.clear()
        root.state(newstate= 'normal')
        #print("DEBUGTEST6")
        
    def random():
        window.destroy()
        shuffle(allPieceList)
        mySystemState.pieces_found(allPieceList[0].position)
        print(mySystemState.state)
        mySystemState.move_robot()
        print(mySystemState.state)
        mySystemState.drop_piece()
        print(mySystemState.state)
        mySystemState.move_home()
        print(mySystemState.state)
        allPieceList.pop(0)
        
        for piece in allPieceList:
            print(piece.position)
            print(piece.shape)
            print(piece.color)
            mySystemState.not_all_pieces_dropped(piece.position)
            print(mySystemState.state)
            mySystemState.move_robot()
            print(mySystemState.state)
            mySystemState.drop_piece()
            print(mySystemState.state)
            mySystemState.move_home()
            print(mySystemState.state)
            
        bluePieceList.clear()
        greenPieceList.clear()
        yellowPieceList.clear()
        allPieceList.clear()
        root.state(newstate= 'normal')        
                
    def target():
        window.destroy()
        try:
            number = askstring('input', 'which piece number do you want to pick?')
            numberCheck = number.isnumeric()
            targeted_piece = int(number)
            if not numberCheck:
                raise TypeError
        except TypeError:
            print("Only numbers allowed")
        else:
            mySystemState.pieces_found(allPieceList[targeted_piece].position)
            print(mySystemState.state)
            mySystemState.move_robot()
            print(mySystemState.state)
            mySystemState.drop_piece()
            print(mySystemState.state)
            mySystemState.move_home()
            print(mySystemState.state)
            print("Piece finished picking")
        finally:
            root.state(newstate= 'normal')
    
    bluePieceList.clear()
    greenPieceList.clear()
    yellowPieceList.clear()
    allPieceList.clear()
    root.state(newstate= 'iconic')
    mySystemState.startbutton_pressed()
    
    #if no pieces found, do nothing
    if not allPieceList:
        mySystemState.no_pieces_found()
        root.state(newstate= 'normal')
    
    else:            
        window= tk.Tk()
        window.title('Operation Mode')
        window.attributes('-topmost', True)
        window.resizable(False, False)
        myFont1 = font.Font(family= 'Helvetica', size= 30, weight= 'bold')
        
        main_button = tk.Button(window, text= 'Main', command= main, height= 1, fg= 'white', bg= 'red')
        main_button['font'] = myFont1
        main_button.grid(column= 1, row= 0, sticky= tk.N, padx= 15, pady= 15, ipadx= 15)
        
        random_button = tk.Button(window, text= 'Random', command= random, height= 1, fg= 'white', bg= 'red')
        random_button['font'] = myFont1
        random_button.grid(column=2, row= 0, sticky= tk.N, padx= 15, pady= 15)
        
        target_button = tk.Button(window, text= 'Target', command= target, height= 1, fg= 'white', bg= 'red')
        target_button['font'] = myFont1
        target_button.grid(column= 1, row= 1, sticky= tk.S, padx= 15, pady= 15)
        
        exit_button = tk.Button(window, text='Exit', command= lambda: window.destroy(), height= 1, fg= 'white', bg= 'red')
        exit_button['font'] = myFont1
        exit_button.grid(column= 2, row= 1, sticky= tk.S, padx= 15, pady= 15, ipadx= 45)
        
        tk.mainloop()
        
    cv2.destroyAllWindows()
        

if __name__ == "__main__":
    #create Camera piece with guessed resolution
    myCamera=Camera([1920,1080])
    #create system state object
    mySystemState = SystemState()
    #create Robot object
    myRobot = Robot()
    
    root = tk.Tk()
    root.title('RobotArm')
    root.attributes("-topmost", True)
    root.resizable(False, False)
    myFont = font.Font(family= 'Helvetica', size= 30, weight= 'bold')
        
    start_button = tk.Button(root, text= 'Start', command= start, height= 1, fg= 'white', bg= 'red')
    start_button['font'] = myFont
    start_button.grid(column= 0, row = 0, sticky= tk.N, padx= 15, pady= 15, ipadx= 15)
    
    exit_button = tk.Button(root, text='Exit', command= lambda: root.destroy(), height= 1, fg= 'white', bg= 'red')
    exit_button['font'] = myFont
    exit_button.grid(column= 1, row= 0, sticky= tk.N, padx= 15, pady= 15, ipadx= 20)
    
    tk.mainloop()