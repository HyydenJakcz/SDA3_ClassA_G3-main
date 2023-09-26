import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)

mask_area_thres = 100

while True:

    _,frame = cap.read()

    Cropped_frame=frame[180:370,270:445]

    scale_factor=3  #Makes the cropped mask x times bigger
    scaled_frame = cv2.resize(Cropped_frame, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

    hsv = cv2.cvtColor(scaled_frame, cv2.COLOR_BGR2HSV)

    low_yellow = np.array([25, 70, 120])
    up_yellow = np.array([30, 255, 255])

    low_green = np.array([40, 70, 80])
    up_green = np.array([70, 255, 255])

    low_red = np.array([159, 115, 115])
    up_red = np.array([180, 255, 255])

    low_blue = np.array([90, 60, 70])
    up_blue = np.array([140, 255, 255])

    bmask = cv2.inRange(hsv, low_blue, up_blue)
    gmask = cv2.inRange(hsv, low_green, up_green)
    rmask = cv2.inRange(hsv, low_red, up_red)
    ymask = cv2.inRange(hsv, low_yellow, up_yellow)

    contours_b = cv2.findContours(bmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_b =imutils.grab_contours(contours_b)

    contours_g = cv2.findContours(gmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_g =imutils.grab_contours(contours_g)

    contours_r = cv2.findContours(rmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_r =imutils.grab_contours(contours_r)

    contours_y = cv2.findContours(ymask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_y =imutils.grab_contours(contours_y)

    for c in contours_b:
        area_b = cv2.contourArea(c)
        if area_b >mask_area_thres:
        
            cv2.drawContours(scaled_frame, [c], -1, (255,255,255), 3)

            M = cv2.moments(c)

            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])

            cv2.circle(scaled_frame, (cx, cy), 7, (255,255,255), -1)
            cv2.putText(scaled_frame, "Blue", (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)


    for c in contours_g:
        area_g = cv2.contourArea(c)
        if area_g >mask_area_thres:
        
            cv2.drawContours(scaled_frame, [c], -1, (255,255,255), 3)

            M = cv2.moments(c)

            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])

            cv2.circle(scaled_frame, (cx, cy), 7, (255,255,255), -1)
            cv2.putText(scaled_frame, "Green", (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)

    for c in contours_r:
        area_r = cv2.contourArea(c)
        if area_r >mask_area_thres:
        
            cv2.drawContours(scaled_frame, [c], -1, (255,255,255), 3)

            M = cv2.moments(c)

            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])

            cv2.circle(scaled_frame, (cx, cy), 7, (255,255,255), -1)
            cv2.putText(scaled_frame, "Red", (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)

    for c in contours_y:
        area_y = cv2.contourArea(c)
        if area_y >mask_area_thres:
        
            cv2.drawContours(scaled_frame, [c], -1, (255,255,255), 3)

            M = cv2.moments(c)

            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])

            cv2.circle(scaled_frame, (cx, cy), 7, (255,255,255), -1)
            cv2.putText(scaled_frame, "Yellow", (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)

    cv2.imshow('result', scaled_frame)

    key = cv2.waitKey(20)
    if key == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

