from sense_hat import SenseHat
from time import sleep
from picamera2 import Picamera2, Preview

sense=SenseHat()

while True:
    for event in sense.stick.get_events():
        
        print(event.direction,event.action)
        
        if event.action =="pressed":  ## check if the joystick was pressed
            if event.direction=="middle":   ## to check for other directions use "up", "down", "left", "right"
                
                
                picam2 = Picamera2()
                camera_config = picam2.create_preview_configuration()
                picam2.configure(camera_config)
                picam2.start_preview(Preview.QTGL)
                picam2.start()
                
                sleep(2)
                picam2.capture_file("test.jpg")
                sense.show_message("test.jpg",text_colour=(255,255,255))  ## white color text
                
            sleep(2) ## wait a while and then clear the screen
            sense.clear()
            
            
