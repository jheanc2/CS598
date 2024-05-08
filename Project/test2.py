from roboflow import Roboflow
import cv2
import numpy as np
import time
import mysql.connector

cnx = mysql.connector.connect(
    host = "172.20.10.7",
    user="pi5",
    password="Abc12345678@",
    database="parking_space"
)

cursor = cnx.cursor()
rf = Roboflow(api_key="amUowktgGe1wkxhFplOW")
#workspace = rf.workspace()
#print(workspace)
#model = rf.workspace("computer-vision-n80te").project("parking-lot-dectection-p1qn8").version(2, local="https://detect.roboflow.com").model
model = rf.workspace("computer-vision-sy6ia").project("parking-lot-dectection-rgonx").version(1, local="http://localhost:9001/").model
count = 1

park81 = [(747, 500), (1185, 468), (743, 706), (1270, 708)]
park82 = [(113, 459), (634, 458), (37, 712), (618, 700)]
park83 = [(698, 131), (995, 98), (694, 407), (1051, 372)]
park84 = [(302, 154), (657, 132), (314, 393), (650, 395)]

frame = 1
while True:
    try:
        prediction = model.predict(f"./time_frame/{frame}.png", confidence=50)
        #print(prediction.json())
        print(len(prediction))
        count = [0, 0, 0, 0]
        for bounding_box in prediction:
            sql = "UPDATE Availability SET Status = %s WHERE SpotID = %s" 
            x1 = bounding_box['x'] - bounding_box['width'] / 2
            x2 = bounding_box['x'] + bounding_box['width'] / 2
            y1 = bounding_box['y'] - bounding_box['height'] / 2
            y2 = bounding_box['y'] + bounding_box['height'] / 2
            box = (x1, x2, y1, y2)
            cx = int(x1+x2)//2
            cy = int(y1+y2)//2
            #print(cx, cy)
            
            if cx > 640 and cy > 360:
                print("Parking space 81 has a car!")
                count[0] = 1
            if cx > 640 and cy < 360:
                print("Parking space 83 has a car!")
                count[2] = 1
            
            if cx < 640 and cy > 360:
                print("Parking space 82 has a car!")
                count[1] = 1
            if cx < 640 and cy < 360:
                print("Parking space 84 has a car!")
                count[3] = 1
            
        for i in range(4):
            SpotID = 81+i
            if count[i] == 1:
                print("Updata spot occupied", SpotID)
                new_status = 2
                cursor.execute(sql,(new_status, SpotID))
                cnx.commit()
            else:
                print("Updata spot empty", SpotID)
                new_status = 1
                cursor.execute(sql,(new_status, SpotID))
                cnx.commit()
            #result81 = cv2.pointPolygonTest(np.array(park81, np.int32),((cx, cy)), False)
            #result82 = cv2.pointPolygonTest(np.array(park82, np.int32),((cx, cy)), False)
            #result83 = cv2.pointPolygonTest(np.array(park83, np.int32),((cx, cy)), False)
            #result84 = cv2.pointPolygonTest(np.array(park84, np.int32),((cx, cy)), False)
            #print(result81, result82, result83,result84)
            #if result81>= 0: 
            #    print("Parking space 81 has a car!")
            #if result82>= 0: 
            #    print("Parking space 82 has a car!")
            #if result83>= 0: 
            #    print("Parking space 83 has a car!")
            #if result84>= 0: 
            #    print("Parking space 84 has a car!")
        
    except:
        print("can't read the png, wait a minute")
        time.sleep(1)
    
cursor.close()
cnx.close()
    #count +=1
    #if count == 16:
    #    count = 1
    #prediction.save("./Prediction/output"+str(i+1)+".png")																	
