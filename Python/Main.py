import cv2
import numpy as np
import serial
from time import sleep
import struct

ser = serial.Serial('/dev/cu.usbmodem14101',9600)
sleep(2)

# Initialize webcam
#cap = cv2.VideoCapture(1)

# define range of RED color in HSV
lower_red1 = np.array([0,120,70])
upper_red1 = np.array([10,255,255])
lower_red2 = np.array([170,120,70])
upper_red2 = np.array([180,255,255])

dist=[]
count = 0
distcount = 0
avg = 0

b = ser.readline()
string_n = b.decode()  # decode byte string into Unicode  
string = string_n.rstrip() # remove \n and \r
flt = int(string) 
print ('Received: ', flt)
sleep(.1)

flt2 = 40000


# loop until break statement is exectured
while (flt == 20000 and flt2 == 40000):

    cap = cv2.VideoCapture(1)

    sleep(3)
    #cap.set(28, 100)

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

        #approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c,True),True)

        

        # If contours are too small or large, ignore them:
        if cv2.contourArea(c)<200:
            continue
        elif cv2.contourArea(c)>1000:
            continue       
##        elif len(approx) > 4:
##            continue
##        elif len(approx) < 4:
##            continue 
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
##        if(count < 10):
##            dist.insert(count, D)

        #print(dist)
        
    ##avg = np.mean(dist)
    ##if(avg > 0):
        val = round(D)
        print (val)
        test = val*255/1300
        test = round (test)
        ser.write(struct.pack('>B', ((int)(test))))
        sleep(5)

    #readval = (int)(ser.readline())

    b1 = ser.readline()
    string_n1 = b1.decode()  # decode byte string into Unicode  
    string1 = string_n1.rstrip() # remove \n and \r
    flt2 = int(string1) 
    print ('Received: ', flt2)
    sleep(.1)
    
    
    # Perform Bitwise AND on mask and our original frame
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('Original2', frame)  
    #cv2.imshow('mask', gray)
    #cv2.imshow('Filtered Color Only', res)

    cap.release()
    
    if cv2.waitKey(1) == 13: #13 is the Enter Key
        break

    count = count + 1
        
cap.release()
cv2.destroyAllWindows()
