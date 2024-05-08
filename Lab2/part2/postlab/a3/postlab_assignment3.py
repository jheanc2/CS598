import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv('rssi4.csv')
df_joy = pd.read_csv('joystick2.csv')

x = df['timestamp']
y = df['rssi']

x_j = df_joy['timestamp']
y_j = df_joy['key']

print(x)
print(x_j)
#df['diff_time'] = df['timestamp'] - df['timestamp'].iloc[0]

time_index = df.index[df['timestamp'].isin(df_joy['timestamp'])].tolist()
matching_rssi = pd.merge_asof(df_joy, df, on='timestamp', direction = 'nearest')


matching_rssi['timestamp'] = matching_rssi['timestamp'] - matching_rssi['timestamp'].iloc[0]
print(matching_rssi)

x_ori, y_ori = 0, 0

direction = np.array([0,1])
path_x, path_y, colors = [x_ori], [y_ori], [matching_rssi['rssi'][0]]

for step, rssi in zip(matching_rssi['key'], matching_rssi['rssi']):
    if step == 'up':
       x_ori, y_ori = x_ori + 0, y_ori + 1
    elif step == 'right':
       x_ori, y_ori = x_ori + 1, y_ori + 0
    elif step == 'left':
       x_ori, y_ori = x_ori -1, y_ori + 0
    elif step == 'down':
       x_ori, y_ori = x_ori + 0, y_ori -1
    else:
       x_middle, y_middle = x_ori, y_ori
       
    path_x.append(x_ori)
    path_y.append(y_ori)
    colors.append(rssi)
    

plt.scatter(path_x, path_y, c = colors, cmap = 'viridis')
plt.plot(x_middle, y_middle,'x',color='red', markersize = 10)
plt.colorbar(label='RSSI Value')
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.title('Walking path with RSSI color coding')
#ax.axvline(x = l, color = 'green', linestyle = '--', label = 'label')
#ax.axvline(x = e_w, color = 'blue', linestyle = '--', label = 'spy end')
#plt.xticks(rotation = 90)
#plt.legend()
plt.show()




