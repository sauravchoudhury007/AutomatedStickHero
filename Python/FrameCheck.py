import cv2
import numpy as np
import serial
from time import sleep
import struct

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
cap.set(cv2.CAP_PROP_FPS, 60)

while (True):

    cap.set(28,200)
   
    
    ret, frame = cap.read()

    cv2.imshow('Original', frame)

    if cv2.waitKey(1) == 13: #13 is the Enter Key
        break

cap.release()
cv2.destroyAllWindows()

