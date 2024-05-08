from sense_hat import SenseHat
from time import sleep
import matplotlib.pyplot as plt

sense=SenseHat()
blue= (0,0,255)
yellow= (255,255,0)
#red=(255,0,0)

sense.clear() ## to clear the LED matrix
t_sum = []
ma = []
tmp = 0
w_size = 5
for i in range(0, 100):
    temperature=sense.get_temperature()
    sleep(0.1)
    #temperature=round(temperature,1)  ## round temperature to 1 decimal place
    t_sum.append(temperature)
    
for i in range(len(t_sum)-w_size+1):
    window = t_sum[i:i+w_size]
    ma.append(sum(window)/w_size)

plt.figure(figsize = (10,6))
plt.plot(range(100),t_sum)
plt.plot(range(len(ma)),ma)
plt.show()


sense.clear()