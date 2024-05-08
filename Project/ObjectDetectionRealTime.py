import time
import datetime

import numpy as np 
import time
from picamera2 import Picamera2
#from picamera2.encoders import H264Encoder
#from picamera2.outputs import CircularOutput
#from libcamera import controls
#from roboflow import Roboflow

import cv2
picam2=Picamera2()  ## Create a camera object

rf = Roboflow(api_key="amUowktgGe1wkxhFplOW")
model = rf.workspace("computer-vision-sy6ia").project("parking-lot-dectection-rgonx").version(1, local="http://localhost:9001/").model

dispW=1280
dispH=720
## Next, we configure the preview window size that determines how big should the image be from the camera, the bigger the image the more the details you capture but the slower it runs
## the smaller the size, the faster it can run and get more frames per second but the resolution will be lower. We keep 
picam2.preview_configuration.main.size= (dispW,dispH)  ## 1280 cols, 720 rows. Can also try smaller size of frame as (640,360) and the largest (1920,1080)
## with size (1280,720) you can get 30 frames per second

## since OpenCV requires RGB configuration we set the same format for picam2. The 888 implies # of bits on Red, Green and Blue
picam2.preview_configuration.main.format= "RGB888"
picam2.preview_configuration.align() ## aligns the size to the closest standard format
picam2.preview_configuration.controls.FrameRate=30 ## set the number of frames per second, this is set as a request, the actual time it takes for processing each frame and rendering a frame can be different

picam2.configure("preview")
## 3 types of configurations are possible: preview is for grabbing frames from picamera and showing them, video is for grabbing frames and recording and images for capturing still images.


picam2.start()

while True:
    #tstart=time.time()
    frame=picam2.capture_array() ## frqame is a large 2D array of rows and cols and at intersection of each point there is an array of three numbers for RGB i.e. [R,G,B] where RGB value ranges from 0 to 255
    
    prediction = model.predict(frame, confidence=50)
    for bounding_box in prediction:
        x, y, w, h = bounding_box['x'], bounding_box['y'], bounding_box['width'], bounding_box['height']
       cv2.rectangle(frame, (x-w/2, y-h/2), (x+w/2, y+h/2), (255,0,0),3)
       time.sleep(0.1)
        
    cv2.imshow("CAmera Frame",frame)
    key=cv2.waitKey(1) & 0xFF
    ## the above command will only grab the frame
    
    #cv2.imshow("piCamera2", frame) ## show the frame
    
    #key=cv2.waitKey(1) & 0xFF
    
    #if key ==ord(" "):
    #    cv2.imwrite("frame-" + str(time.strftime("%H:%M:%S", time.localtime())) + ".jpg", frame)
    if key == ord("q"): ## stops for 1 ms to check if key Q is pressed
        break
    if(len(prediction)>0):
        print("detected cars:",len(prediction))
cv2.destroyAllWindows()  



