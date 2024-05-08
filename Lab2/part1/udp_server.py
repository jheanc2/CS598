import socket

# Binding to 0.0.0.0 allows UDP connections to any address
# that the device is using
UDP_IP = "0.0.0.0"
UDP_PORT = 5000

sock = socket.socket(socket.AF_INET, # Use Internet socket family
                     socket.SOCK_DGRAM) # Use UDP packets
addr = (UDP_IP, UDP_PORT)
