from roboflow import Roboflow
import cv2
import numpy as np
import time
import mysql.connector

cnx = mysql.connector.connect(
    host = "172.20.10.7",
    user="pi5",
    password="Abc12345678@",
    database="parking_space",
    port = '3306'
    
)