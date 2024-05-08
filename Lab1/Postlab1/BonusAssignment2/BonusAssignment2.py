#from sense_hat import SenseHat
#from time import sleep
#import os
#import socket
#import struct
#import fcntl
#import urllib.request

#def get_ip(ifname):
#    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    print(s)
#    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])
#sense=SenseHat()
#blue= (0,0,255)
#yellow= (255,255,0)
#red=(255,0,0)
#hostname  = socket.gethostname()
#ip  = socket.gethostbyname(hostname)
#external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
#print(external_ip)

#try:
#    ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
#    sense.show_message(ip, text_colour=blue, scroll_speed=0.08)
    #print(ip)
        
#except:
#    sense.show_message("can't find ip", text_colour=blue, scroll_speed=0.08)
    #print("can't find ip")
#sense.clear()
