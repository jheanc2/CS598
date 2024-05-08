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

fig, ax = plt.subplots()
ax.plot(df['diff_sec'], y, linewidth=2.0)
plt.xticks(rotation = 90)
plt.show()

