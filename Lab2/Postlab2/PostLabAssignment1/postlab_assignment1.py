import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv('rssi2.csv')


x = df['timestamp']
y = df['rssi']

df['datetime'] = pd.to_datetime(x,format="%d/%m/%Y,%H:%M:%S.%f")
df['diff_time'] = df['datetime'] - df['datetime'].iloc[0]
df['diff_sec'] = df['diff_time'].dt.total_seconds()
#print(df['diff_sec'])


window_size = 3
df['rssi_smooth'] = df['rssi'].rolling(window = window_size, center = True).mean()

peak_idex = df['rssi_smooth'].idxmax()
peak_time = df['diff_sec'][peak_idex]

s_w = peak_time - window_size/2
e_w = peak_time + window_size/2


fig, ax = plt.subplots()
ax.plot(df['diff_sec'], y, linewidth=2.0)
plt.xlabel('Time(sec)')
plt.ylabel('RSSI(dB)')
plt.title('RSSI values over time')
ax.axvline(x = s_w, color = 'green', linestyle = '--', label = 'spy start')
ax.axvline(x = e_w, color = 'blue', linestyle = '--', label = 'spy end')
plt.xticks(rotation = 90)
plt.legend()
plt.show()


