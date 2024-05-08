from sense_hat import SenseHat
from time import sleep

sense=SenseHat()
blue= (0,0,255)
yellow= (255,255,0)
#red=(255,0,0)

sense.clear() ## to clear the LED matrix
temperature_o=sense.get_temperature()
temperature_o=round(temperature_o,1)  ## round temperature to 1 decimal place

while(1):
    #sense.show_message("Welcome to CS 437")
    pressure=sense.get_pressure()
    temperature=sense.get_temperature()
    temperature=round(temperature,1)  ## round temperature to 1 decimal place
    humidity=sense.get_humidity()
    
    #sense.show_letter("R", red)
    #sleep(1)
    #print("The air pressure is",pressure, "millibars")
    print("The air temperature is", temperature, "celcius")
    #print("The humidity is", humidity, "%")
    sense.show_message("p:"+str(pressure)+"t:"+str(temperature)+"h:"+str(humidity), text_colour=blue, scroll_speed=0.05)
    if abs(temperature-temperature_o) >= 1:
        break
while(1):
    sense.set_pixel(3,3, (255, 0, 0))
    sleep(1)
    sense.set_pixel(3,3, (255, 255, 255))
    sleep(1)
sense.clear()
