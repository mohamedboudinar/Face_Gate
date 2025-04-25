import cv2
import os


PATH_SAVE_IMAGES="C:/Users/iness/Downloads/projekt/"
# Create a directory to save the images
save_dir = 'images'
if not os.path.exists(PATH_SAVE_IMAGES):
    os.exit(1)

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

    # Display the frame
    cv2.imshow('Capture Images', frame)

    # Save the frame as an image file
    img_path = os.path.join(PATH_SAVE_IMAGES, f'image_{img_count}.jpg')
    cv2.imwrite(img_path, frame)
    print(f'Saved: {img_path}')

    img_count += 1

    # Wait for 1 second before capturing the next image
    cv2.waitKey(2000)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
