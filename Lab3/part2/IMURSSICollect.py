from sense_hat import SenseHat
import numpy as np
import time
import scipy.signal as signal
from datetime import datetime,date
import matplotlib.pyplot as plt
import pandas as pd
import asyncio
from scapy.all import *
import csv
import scipy.integrate as integrate
path="/home/pi/Downloads/Lab3/part2/" # Change the path to your current folder (you can use `pwd` command in terminal to find the full path)
sense=SenseHat()


timestamp_fname=datetime.now().strftime("%H:%M:%S")
sense.set_imu_config(True,True,True) ## Config the Gyroscope, Accelerometer, Magnetometer
filename=path+timestamp_fname+".csv"
# Variables to be modified
dev_mac = "d8:3a:dd:01:ce:8d"  # Change to a hidden camera's MAC
iface_n = "wlan1"  # Interface for network adapter (do not modify)
rssi_file_name = path+timestamp_fname+"_rssi.csv"  # Output RSSI CSV file name

global_rssi = 0 
def create_rssi_file():
    """Create and prepare a file for RSSI values"""
    header = ["timestamp", "dest", "src", "rssi"]
    with open(rssi_file_name, "w", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
def write_to_file(file_name, data):
    """Write data to a file"""
    with open(file_name, "a", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(data)
def captured_packet_callback(pkt):
    """Save MAC addresses, time, and RSSI values to CSV file if MAC address of src matches.
    
    Example output CSV line:
    2024/02/11,11:12:13.12345, 1707692954.1, 00-B0-D0-63-C2-26, 00:00:5e:00:53:af, -32.2
    """
    cur_dict = {}
    # Check pkt for dst, src, and RSSI field
    try:
        cur_dict["mac_1"] = pkt.addr1
        cur_dict["mac_2"] = pkt.addr2
        cur_dict["rssi"] = pkt.dBm_AntSignal
        
        #print(cur_dict)
    except AttributeError:
        return  # Ignore packet without RSSI field

    date_time = datetime.now().strftime("%d/%m/%Y,%H:%M:%S.%f")  # Get current datetime
    timestamp = time.time()
    #print(date_time, cur_dict)
    # @TODO: Filter packets with src = the hidden camera's MAC
    if cur_dict["mac_2"] == dev_mac:
        
        global global_rssi
        global_rssi = cur_dict["rssi"]
        print(date_time, global_rssi)
        #write_to_file(rssi_file_name,(timestamp, cur_dict["mac_1"],cur_dict["mac_2"],cur_dict["rssi"]))
if __name__ == "__main__":
    
    t = AsyncSniffer(iface=iface_n, prn=captured_packet_callback, store=0)
    t.daemon = True
    t.start()
    
    with open(filename,"w") as f:
        print("collecting data now")
        while True:
            accel=sense.get_accelerometer_raw()  ## returns float values representing acceleration intensity in Gs
            orient=sense.get_orientation_radians()  ## returns float values representing rotation of the axis in radians
            mag=sense.get_compass_raw()  ## returns float values representing magnetic intensity of the ais in microTeslas
            gyro=sense.get_gyroscope_raw()
        
            x=accel['x']
            y=accel['y']
            z=accel['z']
            pitch = orient['pitch']
            roll = orient['roll']
            yaw = orient['yaw']
            gyro_x=gyro['x']
            gyro_y=gyro['y']
            gyro_z=gyro['z']
            if global_rssi:
                rssi = global_rssi
            else:
                rssi = 0
            timestamp=datetime.now().strftime("%H:%M:%S")
            entry= str(time.time())+","+timestamp+","+str(x)+","+str(y)+","+str(z)+","+ str(pitch)+ ","+str(roll)+","+ str(yaw)+ ","+ str(mag['x'])+ ","+str(mag['y'])+","+ str(mag['z'])+","+str(gyro_x)+","+str(gyro_y)+","+str(gyro_z)+","+str(rssi)+"\n"#14
            
            f.write(entry)
       
            
    f.close()
    t.stop()
        



