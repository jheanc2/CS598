import numpy as np
import time
from datetime import datetime,date
import matplotlib.pyplot as plt
import pandas as pd
import csv
## Install the following libraries if they are not already installed on your Raspi:
## pip3 install seaborn
## sudo apt-get install python3-pandas
## sudo apt-get install python3-matplotlib

class KalmanFilter:
    def __init__(self, dt, process_noise_covariance, measurement_noise_covariance):
        self.F = np.array([[1, dt, 0 ,0 ,0 ,0],
                           [0, 1 ,dt ,0, 0 ,0],
                           [0, 0, 1 ,dt ,0 ,0],
                           [0, 0, 0 ,1 ,dt ,0],
                           [0, 0, 0 ,0 ,1 ,dt],
                           [0, 0, 0 ,0 ,0 ,1]])
        
        self.H = np.array([[1, 0, 0 ,0 ,0 ,0],
                           [0, 0, 1 ,0 ,0 ,0],
                           [0, 0, 0 ,0 ,1, 0]])
        
        
        self.Q = process_noise_covariance
        self.R = measurement_noise_covariance
        self.x = np.zeros(6)
        self.P = np.eye(6)
    
    def predict(self):
        self.x = np.dot(self.F, self.x)
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q
        
    def update(self, z):
         K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(np.dot(np.dot(self.H, self.P), self.H.T) + self.R))
         self.x = self.x + np.dot(K, (z - np.dot(self.H, self.x)))
         self.P = np.dot((np.eye(6) - np.dot(K, self.H)), self.P)
    
filename="/home/pi/Downloads/Lab3/prelab/18:15:38.csv"

## CSV file template:
# time in seconds, timestamp (H:M:S), X-Accel, Y-Accel, Z-Accel, pitch, roll, yaw, X-Mag, Y-Mag, Z-Mag, X-Gyro, Y-Gyro, Z-Gyro


df =pd.read_csv(filename, header=None)
df=df.dropna()

timestamp = df[0]

timestamps2=df[1]
x_axis=df[2]
y_axis=df[3]
z_axis=df[4]
plt.plot(x_axis,  label="X-axis Raw Acceleration")
plt.plot(y_axis,  label="Y-axis Raw Acceleration")
plt.plot(z_axis,  label="Z-axis Raw Acceleration")
plt.legend(loc="upper left")
plt.ylabel("Raw Acceleration in m/s^2")
plt.xlabel("Number of Data Points")
plt.show()

### CALIBERATION
x_calib_mean = np.mean(x_axis[1:100])
## caliberate x,y,z to reduce the bias in accelerometer readings. Subtracting it from the mean means that in the absence of motion, the accelerometer reading is centered around zero to reduce the effect of integrigation drift or error.
## change the upper and lower bounds for computing the mean where the RPi is in static position at the begining of the experiment (i.e. for the first few readings). You can know these bounds from the exploratory plots above.
x_calib = x_axis - x_calib_mean
x_calib = x_calib[:]
timestamp = timestamp[:]

y_calib_mean = np.mean(y_axis[1:100])
y_calib = y_axis - y_calib_mean
y_calib = y_calib[:]
timestamp = timestamp[:]

z_calib_mean = np.mean(y_axis[1:100])
z_calib = z_axis - z_calib_mean
z_calib = z_calib[:]
timestamp = timestamp[:]

plt.plot(x_calib, label="X-axis Caliberated Acceleration")
plt.plot(y_calib, label="Y-axis Caliberated Acceleration")
plt.plot(z_calib, label="Z-axis Caliberated Acceleration")
plt.legend(loc="upper left")
plt.ylabel("Caliberated Acceleration in m/s^2")
plt.xlabel("Number of Data Points")
plt.show()


print("Check if lengths of each vector are same for tracking time", len(timestamp), len(x_calib), len(y_calib), len(z_calib))
# Find sampling time:
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

plt.plot(x_vel, label="X-axis velocity")
plt.plot(y_vel, label="Y-axis velocity")
plt.legend(loc="upper left")
plt.ylabel("Velocity in m/s")
plt.xlabel("# of Samples")
plt.show()

x = [0]

for i in range(len(x_vel)-1):
    x.append(x[-1] + dt * x_vel[i])
    
## Integrations along Z axis:

z_vel = [0]
for i in range(len(z_calib)-1):
    z_vel.append(z_vel[-1] + dt * z_calib[i])

#plt.plot(z_vel)

z = [0]
plt.figure()
for i in range(len(z_vel)-1):
    z.append(z[-1] + dt * z_vel[i])
#plt.plot(z)

## Plot X and Y positions with respect to time:
plt.plot(timestamp,x, label="X positions", c="red")
plt.plot(timestamp,y, label="Y positions", c="green")
plt.legend(loc="upper left")
plt.xlabel("Timestamp (seconds)")
plt.ylabel("Positions (m)")
plt.show()


accelerations = []
estimate_pos = []
estimate_vel = []

for a_x, a_y, a_z in zip(x_calib, y_calib, z_calib):
    accelerations.append([a_x, a_y, a_z])
accelerations = np.array(accelerations)
pnc = np.eye(6) * 0.01
mnc = np.eye(3) * 0.1
kf = KalmanFilter(dt, pnc, mnc)
for accel in accelerations:
    kf.predict()
    kf.update(accel)
    
    estimate_pos.append(kf.x[:3])
    estimate_vel.append(kf.x[3:])
estimate_pos = np.array(estimate_pos)
estimate_vel = np.array(estimate_vel)

win = 30
smooth_x = pd.Series(estimate_pos[:,0]).rolling(window = win).mean()
smooth_y = pd.Series(estimate_pos[:,1]).rolling(window = win).mean()
print(len(smooth_x))
plt.plot(smooth_x,smooth_y, label="Y positions", c="green")
plt.legend(loc="upper left")
plt.xlabel("Timestamp (seconds)")
plt.ylabel("Positions (m)")
plt.show()
## Visualizing scatter plot in 2D. Fill in if you want to see this data

##

## Orientation Integration

yaw = df[7]
plt.plot(yaw)
plt.show()

x_vel_corrected = [0]
y_vel_corrected = [0]
x_dir_corrected = [0]
y_dir_corrected = [0]
rssis = df[14]
for i in range(len(x_calib)-1):
    x_vel_corrected.append(x_vel_corrected[-1]*np.cos(yaw[i]) + dt * x_calib[i])
    
for i in range(len(y_calib)-1):
    y_vel_corrected.append(y_vel_corrected[-1]*np.sin(yaw[i]) + dt * y_calib[i])
    
for i in range(len(x_vel_corrected)-1):
    x_dir_corrected.append(x_dir_corrected[-1] + dt * x_vel_corrected[i])
    
for i in range(len(y_vel_corrected)-1):
    y_dir_corrected.append(y_dir_corrected[-1] + dt * y_vel_corrected[i])
#for i in range(len(x_calib)-1):
#    x_vel_corrected.append(x_vel[-1]*np.cos(yaw[i]) + dt * x_calib[i])
    
#for i in range(len(y_calib)-1):
#    y_vel_corrected.append(y_vel[-1]*np.sin(yaw[i]) + dt * y_calib[i])
    
#for i in range(len(x_vel_corrected)-1):
#    x_dir_corrected.append(x_dir_corrected[-1] + dt * x_vel_corrected[i])
    
#for i in range(len(y_vel_corrected)-1):
#    y_dir_corrected.append(y_dir_corrected[-1] + dt * y_vel_corrected[i])
    
plt.plot(timestamp,x, label="X positions", c="red")
plt.plot(timestamp,y, label="Y positions", c="green")
plt.plot(timestamp,x_dir_corrected, label="X positions Corrected")
plt.plot(timestamp,y_dir_corrected, label="Y positions Corrected")
plt.legend(loc="upper left")
plt.xlabel("Timestamp (seconds)")
plt.ylabel("Positions (m)")
plt.show()

win = 20
x_dir_corrected = pd.Series(x_dir_corrected).rolling(window = win).mean()
y_dir_corrected = pd.Series(y_dir_corrected).rolling(window = win).mean()
plt.scatter(x_dir_corrected, y_dir_corrected, c = rssis, cmap = 'viridis')
#plt.scatter(x, y, c = rssis, cmap = 'viridis')
plt.colorbar(label='RSSI Value')
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.axis('equal')
plt.title('Walking path with RSSI color coding')
plt.show()

print(len(timestamp),len(x_dir_corrected),len(y_dir_corrected),len(rssis))
combined_column = zip(x_dir_corrected, y_dir_corrected, rssis, timestamp)

# Define the file name for your CSV
csv_file = 'rssi.csv'

# Write the combined data to the CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    for row in combined_column:
        writer.writerow(row)
