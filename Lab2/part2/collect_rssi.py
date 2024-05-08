import csv
from datetime import datetime
from scapy.all import *
import time
import asyncio
from sense_hat import SenseHat

"""
Run monitor_mode.sh first to set up the network adapter to monitor mode and to
set the interface to the right channel.
To get RSSI values, we need the MAC Address of the connection 
of the device sending the packets.
"""

# Variables to be modified
dev_mac = "4a:a9:a6:bd:9f:b5"  # Change to a hidden camera's MAC
iface_n = "wlan1"  # Interface for network adapter (do not modify)
duration = 30  # Number of seconds to sniff for
rssi_file_name = "rssi2.csv"  # Output RSSI CSV file name
joystick_file_name = "joystick.csv"  # Output joystick CSV file name


def create_rssi_file():
    """Create and prepare a file for RSSI values"""
    header = ["timestamp", "dest", "src", "rssi"]
    with open(rssi_file_name, "w", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

def create_joystick_file():
    """Create and prepare a file for joystick input"""
    header = ["timestamp", "key"]
    with open(joystick_file_name, "w", encoding="UTF8") as f:
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

    # @TODO: Filter packets with src = the hidden camera's MAC
    if cur_dict["mac_2"] == dev_mac:
        print(date_time, cur_dict)
    
        write_to_file(rssi_file_name,(date_time, cur_dict["mac_1"],cur_dict["mac_2"],cur_dict["rssi"]))
    # @TODO: Write (timestamp, dest, src, rssi) to the CSV file
    # Hint: Use write_to_file(file_name, data) function to write a list of values to the CSV file


async def record_joystick() -> str:
    """Record joystick input to CSV file"""
    # @TODO: Get joystick input
    return ""


async def main_loop():
    """Main loop to record joystick input and IMU data (in Lab 3)"""
    start = time.time()
    
    while (time.time() - start) < duration:
        # Record joystick input
        key_pressed = await record_joystick()
        if key_pressed:
            # Write (timestamp, key) to the CSV file
            write_to_file(joystick_file_name, [time.time(), key_pressed])

        # Display RSSI reading (in Postlab 2)
        # await display_rssi()


if __name__ == "__main__":
    create_rssi_file()
    create_joystick_file()

    start_date_time = datetime.now().strftime("%d/%m/%Y,%H:%M:%S.%f") #Get current date and time
    print("Start Time: ", start_date_time)

    t = AsyncSniffer(iface=iface_n, prn=captured_packet_callback, store=0)
    t.daemon = True
    t.start()    

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_loop())
    loop.close()

    t.stop()
