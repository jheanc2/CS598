from sense_hat import SenseHat
from time import sleep

sense=SenseHat()
#blue= (0,0,255)
#yellow= (255,255,0)
#red=(255,0,0)
for i in range(0,2):
    #sense.show_message("Welcome to CS 437")
    
    sense.show_message("Welcome to CS 598", text_colour=blue, back_colour=yellow, scroll_speed=0.08)
    #sense.show_letter("R", red)
    #sleep(1)

sense.clear()