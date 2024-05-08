import time
import datetime

import numpy as np 
import time
from picamera2 import Picamera2
#3from picamera2.encoders import H264Encoder
#3from picamera2.outputs import CircularOutput
#from libcamera import controls
#from roboflow import Roboflow

import cv2

drawing = False
start_x, start_y = -1, -1

def RGB(event, x, y, flags, param):
    global drawing, start_x, start_y
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_x, start_y = x, y
    if event == cv2.EVENT_MOUSEMOVE :
        if drawing:
            img_copy = image.copy()
            cv2.imshow('RGB', img_copy)
        colorsBGR = [x, y]
        print(colorsBGR)
    if event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.imshow('RGB', image)
        print("FInal:", start_x, start_y, x, y)
image = cv2.imread("time_frame/15.png")
if image is None:
    print("No image")
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

while True:
    key=cv2.waitKey(1) & 0xFF
    if key == ord("q"): ## stops for 1 ms to check if key Q is pressed
        break
 
cv2.destroyAllWindows()  





