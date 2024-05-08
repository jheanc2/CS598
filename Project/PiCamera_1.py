from picamera2 import Picamera2
import time

# Create a Picamera2 object
picam2 = Picamera2()

# Configure the camera
picam2.start()

# Wait for the camera to adjust to conditions
time.sleep(2)

# Capture an image

picam2.capture_file("./Image_train/1.jpg")
print("Image captured and saved as image.jpg")
