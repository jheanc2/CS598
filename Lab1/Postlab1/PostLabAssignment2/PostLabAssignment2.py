from sense_hat import SenseHat
from time import sleep
from picamera2 import Picamera2, Preview
import cv2

sense=SenseHat()
blue= (0,0,255)
yellow= (255,255,0)
#red=(255,0,0)

sense.clear() ## to clear the LED matrix
temperature_o=sense.get_temperature()
temperature_o=round(temperature_o,1)  ## round temperature to 1 decimal place

while(1):
    temperature=sense.get_temperature()
    temperature=round(temperature,1)  ## round temperature to 1 decimal place
    humidity=sense.get_humidity()
    
    print("The air temperature is", temperature, "celcius")
    if abs(temperature-temperature_o) >= 1:
        break
    
picam2=Picamera2()  ## Create a camera object
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
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

while True:
    #tstart=time.time()
    frame=picam2.capture_array() ## frqame is a large 2D array of rows and cols and at intersection of each point there is an array of three numbers for RGB i.e. [R,G,B] where RGB value ranges from 0 to 255
    
    frameGray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(frameGray,1.3,5)
    
    ## frame[rows,columns] --> is the pixel of each frame
    for face in faces:
        x,y,w,h = face
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
        sleep(0.1)
        
    cv2.imshow("Camera Frame",frame)
    key=cv2.waitKey(1) & 0xFF
    ## the above command will only grab the frame
    
    #cv2.imshow("piCamera2", frame) ## show the frame
    
    #key=cv2.waitKey(1) & 0xFF
    
    #if key ==ord(" "):
    #    cv2.imwrite("frame-" + str(time.strftime("%H:%M:%S", time.localtime())) + ".jpg", frame)
    if key == ord("q"): ## stops for 1 ms to check if key Q is pressed
        break
    #tend= time.time()
    #looptime=tend-tstart
    #fps= 1/looptime ## this is the actual frames per second
    #print("frames per second are",int(fps)) ## if you increase the resolution of the image the fps will go down
    if(len(faces)>0):
        print("detected faces:",len(faces))
cv2.destroyAllWindows()  
sense.clear()