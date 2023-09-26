import numpy as np
import cv2


im = cv2.imread('C:/Users/Gebruiker/OneDrive - Office 365 Fontys/Afbeeldingen/color-shapes.png')

imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(imgray, 200, 255, cv2.THRESH_BINARY)

# visualize the binary image
contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

# draw contours on the original image
im_copy = im.copy()

cv2.drawContours(image=im_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

cv2.imshow('normal',im)
cv2.imshow('grayscale', thresh)
cv2.imshow('contours',im_copy)

cv2.waitKey()
cv2.destroyAllWindows()