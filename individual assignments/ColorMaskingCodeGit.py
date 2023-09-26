import cv2
from cv2 import THRESH_BINARY
import numpy as np
import argparse
import PIL


cX=int(0)
cY=int(0)
#image=cv2.imread('C:/Users/Gebruiker/OneDrive - Office 365 Fontys/Afbeeldingen/color-shapes.png')

#Filters this color. "Threshold" is the range of color detection (+-threshhold to "BGR" values)
bgr=[247, 203, 86]
threshold=100

#Creates 2 arrays  of BGR values and adds and substracts the threshold from each value
#We now have a range of colours that will show up, colors outside the range become black (masking)
minBGR = np.array([bgr[0] - threshold, bgr[1] - threshold, bgr[2] - threshold])
maxBGR = np.array([bgr[0] + threshold, bgr[1] + threshold, bgr[2] + threshold])

# Create a video capture object, in this case we are reading the video from a file
vid_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)

if (vid_capture.isOpened() == False):

  print("Error opening the video file")

# Read fps and frame count
else:

  # Get frame rate information
    # You can replace 5 with CAP_PROP_FPS as well, they are enumerations
  fps = vid_capture.get(5)

  print('Frames per second : ', fps,'FPS')

  # Get frame count
  # You can replace 7 with CAP_PROP_FRAME_COUNT as well, they are enumerations
  frame_count = vid_capture.get(7)
  print('Frame count : ', frame_count)

while(vid_capture.isOpened()):
  # vid_capture.read() methods returns a tuple, first element is a bool
  # and the second is frame
  ret, frame = vid_capture.read()

  if ret == True:

    #Crop square coordinates
    Cropped_frame=frame[140:320,355:515]
    #Scale up the cropped mask
    scale_factor=3  #Makes the cropped mask x times bigger
    scaled_frame = cv2.resize(Cropped_frame, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

    #Create grayscale image for countour detection
    frame_gray = cv2.cvtColor(scaled_frame, cv2.COLOR_BGR2GRAY)
    #apply binary thresholding
    ret, thresh = cv2.threshold(frame_gray, 95, 255, THRESH_BINARY)
    #detect the contours of the binary image using cv2.CHAIN_APROX_NONE
    contouritems, hierarchy= cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    
    #copy frame
    frame_copy = scaled_frame.copy()

    #loop for checking contour area and drawing center point
    for contour in contouritems:
      if cv2.contourArea(contour) > 9000:
        #cv2.drawContours(frame_copy, contour, -1, (255, 255, 255), 1)
        
        #get center points of shapes
        M = cv2.moments(contour)
        #compute the center of the contour
        if M['m00'] != 0:
          cX = int(M["m10"]/M["m00"])
          cY = int(M["m01"]/M["m00"])

          #draw center on the shapes
          cv2.circle(frame_copy, (cX,cY), 2, (255,0,0),-1)
          #cv2.putText(frame_copy, "center", (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

      approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)

      cv2.drawContours(frame_copy,[approx], -1, (0, 255,0), 1)

      # putting shape name at center of each shape
      print(len(approx))
      if len(approx) < 7:
        cv2.putText(frame_copy, 'square', (cX-30, cY-30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
  
      else:
        cv2.putText(frame_copy, 'circle', (cX-30, cY-30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
      
      
         
          



    #isplay images
    #cv2.imshow('Frame', frame)
    cv2.imshow('binary image', thresh) #B&W for contour
    cv2.imshow('contours', frame_copy)


  

    
    # 20 is in milliseconds, try to increase the value, say 50 and observe
    key = cv2.waitKey(20)
    if key == ord('q'):

      break

  else:

    break


# Release the video capture object
vid_capture.release()
cv2.destroyAllWindows()




