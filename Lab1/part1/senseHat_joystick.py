from sense_hat import SenseHat
from time import sleep

sense=SenseHat()

while True:
    for event in sense.stick.get_events():
        
        print(event.direction,event.action)
        
        if event.action =="pressed":  ## check if the joystick was pressed
            if event.direction=="middle":   ## to check for other directions use "up", "down", "left", "right"
                sense.show_letter("M",text_colour=(255,255,255))  ## white color text

                
            sleep(2) ## wait a while and then clear the screen
            sense.clear()
            
            