from roboflow import Roboflow

rf = Roboflow(api_key="amUowktgGe1wkxhFplOW")
#workspace = rf.workspace()
#print(workspace)
#model = rf.workspace("computer-vision-n80te").project("parking-lot-dectection-p1qn8").version(2, local="https://detect.roboflow.com").model
model = rf.workspace("computer-vision-sy6ia").project("parking-lot-dectection-rgonx").version(1, local="http://localhost:9001/").model
for i in range(1):
    prediction = model.predict("./time_frame/"+str(i+1)+".png", confidence=50)
    #print(prediction.json())
    for bounding_box in prediction:
        x1 = bounding_box['x'] - bounding_box['width'] / 2
        x2 = bounding_box['x'] + bounding_box['width'] / 2
        y1 = bounding_box['y'] - bounding_box['height'] / 2
        y2 = bounding_box['y'] + bounding_box['height'] / 2
        box = (x1, x2, y1, y2)
        print(box)
        print((x1+x2)//2, (y1+y2)//2)
    prediction.save("./Prediction/output"+str(i+1)+".png")
    print("Done")