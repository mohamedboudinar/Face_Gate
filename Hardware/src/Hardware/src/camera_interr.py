from picamera2 import Picamera2
from time import sleep
import cv2

# Initialize the camera
picam2 = Picamera2()

# Configure the camera for still capture
camera_config = picam2.create_still_configuration(main={"size": (640, 480), "format": "RGB888"})
picam2.configure(camera_config)

# Start the camera
picam2.start()

# Allow the camera to warm up
sleep(2)

while True: 

    # Capture a frame
    frame = picam2.capture_array()

    cv2.imshow('PiCamera FaceGate', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Close the camera
picam2.stop()
picam2.close()
cv2.destroyAllWindows()

