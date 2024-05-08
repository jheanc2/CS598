from sense_hat import SenseHat


sense=SenseHat()


sense.clear() ## to clear the LED matrix

pressure=sense.get_pressure()

temperature=sense.get_temperature()
temperature=round(temperature,1)  ## round temperature to 1 decimal place

humidity=sense.get_humidity()



print("The air pressure is",pressure, "millibars")

print("The air temperature is", temperature, "celcius")

print("The humidity is", humidity, "%")

