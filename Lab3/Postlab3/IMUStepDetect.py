import numpy as np
import time
import scipy.signal as signal
from datetime import datetime,date
import matplotlib.pyplot as plt
import pandas as pd

import seaborn as sns # visualization






filename="/home/pi/Downloads/Lab3/part2/15:10:13.csv"

## CSV file template:
# time in seconds, timestamp (H:M:S), X-Acceleration, Y-Acceleration, Z-Acceleration, X-Gyroscope,Y-Gyro,Z-Gyro,X-Gyro, Y-Gyro, Z-gyro



df =pd.read_csv(filename, header=None)
df = df[:650]
df=df.dropna()

timestamp = df[0]
x_axis=df[2]
y_axis=df[3]
z_axis=df[4]

## Visualize your Accelerometer Values
#plt.plot(x_axis)
#plt.plot(y_axis)
#plt.plot(z_axis)
#plt.show()



## CALIBERATION
# caliberate x,y,z to reduce the bias in accelerometer readings. Subtracting it from the mean means that in the absence of motion, the accelerometer reading is centered around zero to reduce the effect of integrigation drift or error.
# change the upper and lower bounds for computing the mean where the RPi is in static position at the begining of the experiment (i.

x_calib_mean = np.mean(x_axis[1:50])
x_calib = x_axis - x_calib_mean
x_calib = x_calib[:]
timestamp = timestamp[:]

y_calib_mean = np.mean(y_axis[1:50])
y_calib = y_axis - y_calib_mean
y_calib = y_calib[:]
timestamp = timestamp[:]

z_calib_mean = np.mean(z_axis[1:50])
z_calib = z_axis - z_calib_mean
z_calib = z_calib[:]
timestamp = timestamp[:]



#plt.plot(x_calib)
#plt.plot(y_calib[10:])
#plt.plot(z_axis)

#plt.show()

accel_raw = np.linalg.norm(np.array([x_calib, y_calib, z_calib]), axis=0)
accel = signal.savgol_filter(accel_raw, window_length=11, polyorder=4) ## Same as rolling average --> Savitzky-Golay smoothing
## change the window size as it seems fit. If you keep window size too high it will not capture the relevant peaks/steps

# Plot the original and smoothed data
#plt.figure(figsize=(10, 6))
#plt.subplot(2, 1, 1)
#plt.plot(accel_raw)
#plt.title("Original Data")
#plt.subplot(2, 1, 2)
#plt.plot(accel)
#plt.title("Smoothed Data")
#plt.show()


## Step Detection: The instantaneous peaks in the accelerometer readings correspond to the steps. We use thresholding technique to decide the range of peak values for step detection
# Set a minimum threshold (e.g., 1.0) for peak detection

min_threshold = 0.1   ## Change the threshold (if needed) based on the peak accelerometer values that you observe in your plot above

# Calculate the upper threshold for peak detection as the maximum value in the data
upper_threshold = np.max(accel)

# Define the range for peak detection
my_range = (min_threshold, upper_threshold)

# print("range of Accel. values  for peak detection",my_range)
## Visualize the detected peaks in the accelerometer readings based on the selected range
#plt.plot(accel)

#Use this link to find the peaks: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
peak_array, _ = signal.find_peaks(accel, height = min_threshold) # Enter function here
#plt.plot(peak_array, accel[peak_array], "x", color="r")
#for i, point in enumerate(peak_array):
#    s = str(i+1)
#    plt.text(point, accel[point],s)
#plt.title('step count')
#plt.xlabel('time(s)')
#plt.ylabel('accel(m/s2)')
#plt.show()

# Peak array indices -> peak_array
# Accel values at high peaks --> accel[peak_array]
dt = (timestamp[len(timestamp)-1] - timestamp[0]) / len(timestamp)

## Computing Velocity and Position along Y Axis:
y_vel = [0]
for i in range(len(y_calib)-1):
    y_vel.append(y_vel[-1] + dt * y_calib[i])

y = [0]

for i in range(len(y_vel)-1):
    y.append(y[-1] + dt * y_vel[i])
    
## Integrations along X axis
x_vel = [0]
for i in range(len(x_calib)-1):
    x_vel.append(x_vel[-1] + dt * x_calib[i])

x = [0]

for i in range(len(x_vel)-1):
    x.append(x[-1] + dt * x_vel[i])
    
## Integrations along Z axis:

z_vel = [0]
for i in range(len(z_calib)-1):
    z_vel.append(z_vel[-1] + dt * z_calib[i])

#plt.plot(z_vel)

z = [0]
#plt.figure()
for i in range(len(z_vel)-1):
    z.append(z[-1] + dt * z_vel[i])
#plt.plot(z)

#print(peak_array)
tx=[0]
ty =[0]
for i in peak_array:
    tx.append(x[i])
    ty.append(y[i])
    
## Plot X and Y positions with respect to time:
#plt.scatter(tx,ty, label="positions", c="red")
#plt.legend(loc="upper left")
#plt.xlabel("x")
#plt.ylabel("y")
#plt.axis('equal')
#plt.show()


# Set the orientation/direction of motion (walking direction).
# walking_direction is an angle in degrees with global frame x-axis. It can be from 0 degrees to 360 degrees.
# for e.g. if walking direction is 90 degrees, user is walking in the positive y-axis direction.
# Assuming you are moving along the +X-axis with minor deviations/drifts in Y, we set the orientation to 5 (ideally it should be 0 but to take into account the drifts we keep 5)
# Additionally, we assume that the walking direction will be the same throught the trajectory that you capture in exercise 1.

# This will change for exercise 2
dt = (timestamp[len(timestamp)-1] - timestamp[0]) / len(timestamp)
gyro_z = df[13]
yaw = [0]
yaws = df[7]
#plt.plot(gyro_z)
#plt.show()
for i in range(len(gyro_z)-1):
    yaw.append(yaw[-1] + dt * gyro_z[i])

#walking_dir = np.deg2rad(yaw) ## deg to radians


# To compute the step length, we estimate it to be propertional to the height of the user.

height=1.74 # in meters # Change the height of the user as needed
step_length= 0.24 * height # in meters

# Convert walking direction into a 2D unit vector representing motion in X, Y axis:
angle = np.array([np.cos(yaw), np.sin(yaw)])

## Start position of the user i.e. (0,0)
#cur_position = np.array([0.0, 0.0], dtype=float)
txx = []
tyy = []
count = 0
turn = None
peak_array2 = peak_array
for i in range(len(z_calib)):
    if i in peak_array:
        count += 1
        theta = yaw[i]
        
        if abs(step_length* np.sin(theta)) > abs(step_length* np.cos(theta)):#and ((turn == 'right' and count>2) or (turn != 'right'))
        #    print('increase x ', abs(step_length* np.sin(theta))- abs(step_length* np.cos(theta)))
            txx.append(step_length* np.sin(theta))
            tyy.append(0)
        #    if turn != 'left':
        #        count = 0
        #        turn = 'left'
        else:
        #    print('increase y ',abs(step_length* np.sin(theta))- abs(step_length* np.cos(theta)))
            txx.append(0)
            tyy.append(step_length* np.cos(theta))
        #    if turn != 'right':
        #        count = 0
        #        turn = 'right'
       # 
        #print(turn, count)
        #txx.append(step_length* np.sin(theta))
        #tyy.append(step_length* np.cos(theta))
    else:
        txx.append(0)
        tyy.append(0)
        

txx_acc = [txx[0]]
tyy_acc = [tyy[0]]
for i in range(1,len(txx)):
    txx_acc.append(txx_acc[i-1]+txx[i])
    tyy_acc.append(tyy_acc[i-1]+tyy[i])
    

rssis = df[14]
min_rssi = min(rssis)
rssis[rssis==0] = min_rssi

max_r = np.argmax(np.array(rssis))
indices = np.argsort(np.array(rssis))[-3:][::-1]
mean_x, mean_y = 0,0
for i in indices:
    mean_x += txx_acc[i]
    mean_y += tyy_acc[i]

mean_x, mean_y = mean_x/3, mean_y/3
print("max rssi position",mean_x,mean_y)
plt.scatter(txx_acc,tyy_acc,c = rssis, cmap = 'viridis')
plt.plot(mean_x, mean_y, "x", color="r")
plt.colorbar(label='RSSI Value')
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.axis('equal')
plt.title('Walking path with RSSI color coding')
plt.show()