import cv2
import os

PATH_SAVE_IMAGES = "C:/Users/Mohamed Boudinar/Downloads/testimages/"

# Check if the save directory exists, if not, exit the script
if not os.path.exists(PATH_SAVE_IMAGES):
    print(f"Error: Save directory {PATH_SAVE_IMAGES} does not exist.")
    exit(1)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

img_count = 0
max_images = 10

while img_count < max_images:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        break

    # Resize the frame to 640x480 resolution
    resized_frame = cv2.resize(frame, (640, 480))

    # Display the frame
    cv2.imshow('Capture Images', resized_frame)

    # Save the frame as an image file
    img_path = os.path.join(PATH_SAVE_IMAGES, f'image_{img_count}.jpg')
    cv2.imwrite(img_path, resized_frame)
    print(f'Saved: {img_path}')

    img_count += 1

    # Wait for 2 seconds before capturing the next image
    cv2.waitKey(2000)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
