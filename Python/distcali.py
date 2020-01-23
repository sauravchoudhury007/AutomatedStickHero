import cv2
import numpy as np
import serial
from time import sleep
import struct

# define range of RED color in HSV
lower_red1 = np.array([0,120,70])
upper_red1 = np.array([10,255,255])
lower_red2 = np.array([170,120,70])
upper_red2 = np.array([180,255,255])


# loop until break statement is exectured
while (True):

    cap = cv2.VideoCapture(1)

    # Read webcam image
    ret, frame = cap.read()
 
    # Convert image from RBG/BGR to HSV so we easily filter
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Use inRange to capture only the values between lower & upper_blue
    mask1 = cv2.inRange(hsv_img, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_img, lower_red2, upper_red2)

    mask = mask1 + mask2

    #img_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(mask, 70, 255, cv2.THRESH_BINARY_INV)

    ret2, thresh = cv2.threshold(gray, 127, 255, 1)

    #im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    centers=[]
   
    
    for c in contours:

        # If contours are too small or large, ignore them:
        if cv2.contourArea(c)<200:
            continue
        elif cv2.contourArea(c)>1000:
            continue       
        cv2.drawContours(frame, [c], -1, (0,255,0), 3)

        # Find center point of contours:
        M = cv2.moments(c)
        cX = int(M['m10'] /M['m00'])
        cY = int(M['m01'] /M['m00'])
        centers.append([cX,cY])

        # Find the distance D between the two contours:
    if (len(centers) == 2):
        dx= centers[0][0] - centers[1][0]
        dy = centers[0][1] - centers[1][1]
        D = np.sqrt(dx*dx+dy*dy)
        print(D)
        
    
    # Perform Bitwise AND on mask and our original frame
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('Original2', frame)  
    #cv2.imshow('mask', gray)
    #cv2.imshow('Filtered Color Only', res)

    cap.release()
    
    if cv2.waitKey(1) == 13: #13 is the Enter Key
        break
        
cap.release()
cv2.destroyAllWindows()
