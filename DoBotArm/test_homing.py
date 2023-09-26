import threading
import DoBotArm as Dbt
import time
from serial.tools import list_ports
import numpy as np

#bod dimensions +- extra for scaling
boxHeight = 140+10
boxLength = 120+30

imageHeight = 190
imageLength = 175

def port_selection():
    # Choosing port
    available_ports = list_ports.comports()
    print('Available COM-ports:')
    for i, port in enumerate(available_ports):
        print(f"  {i}: {port.description}")

    choice = int(input('Choose port by typing a number followed by [Enter]: '))
    return available_ports[choice].device

def homing_prompt():
    while (True):
        response = input("Do you wanna home? (y/n)")
        if(response == "y") :
            return True
        elif (response == "n"):
            return False
        else:
            print("Unrecognised response")

#--Main Program--
def main():
    #List selected ports for selection
    port = port_selection()
        
    # Preprogrammed sequence
    homeX, homeY, homeZ = 280, -120, 50
    dropX, dropY, dropZ = 200, 0, 50
    print("Connecting")
    print("Homing")
    ctrlBot = Dbt.DoBotArm(port, homeX, homeY, homeZ, home = True) #Create DoBot Class Object with home position x,y,z 
    
    #move to each corner of the black square
    print("moving to the top-left corner")
    ctrlBot.commandDelay()
    ctrlBot.moveArmXY(140, -120)
    print("wait for 1 secs")
    time.sleep(1)
    print("moving to the bottom left corner")
    ctrlBot.moveArmXYZ(140, -240, 50, wait= True)
    print("wait 1s")
    time.sleep(1)
    print("moving to home")
    ctrlBot.moveHome()
    
    print("wait 1s")
    time.sleep(1)
    
    position = (76, 55)
    rotationMatrix = np.array(((0, -1), 
                              (1, 0)))
    result = np.dot(position, rotationMatrix)
    pointX, pointY = result
    print(result)
    print(homeX, homeY, homeZ)
    
    #scale the movement according to the difference in size of points in real and the image
    moveX = boxLength*pointX/imageLength
    moveY = boxHeight*pointY/imageHeight
    print(moveX, moveY)
    ctrlBot.moveArmRelXY(-moveX, moveY)
    pos = ctrlBot.getPosition()
    print(pos)
    
    #robot picking movement
    #print("moving to center")
    #ctrlBot.moveArmRelXY(70, -70)
    print("wait for 3s")
    time.sleep(3)
    ctrlBot.toggleSuction()
    ctrlBot.moveArmRelXYZ(0,0,-90)
    print("wait for 3s")
    time.sleep(1)
    ctrlBot.moveArmRelXYZ(0, 0, 90)
        
    #robot drops the object
    print("moving to drop point")
    ctrlBot.moveArmXYZ(dropX, dropY, dropZ)
    ctrlBot.toggleSuction()
    time.sleep(1)
    """
    #move the conveyor from left to right
    
    print("moving the conveyor")
    for i in range(250):
        ctrlBot.SetConveyor(enabled= True, speed= 20000)
    ctrlBot.SetConveyor(False)
            
    #move the conveyor from right to left
    print("moving the conveyor")
    for i in range(250):
        ctrlBot.SetConveyor(enabled= True, speed= -20000)
    ctrlBot.SetConveyor(False)
    """
    
    print("Disconnecting")
"""
length of black square: 140
height of black square: 120
dropping coordinates: 200, 0, 50
top left coordinates: 140, -120, 50
top right coordinateS: 280, -120, 50
bottom left coordinates: 140, -240, 50
do not go to the bottom right corner(out of the robot's reach)
"""
 
if __name__ == "__main__":
    main()