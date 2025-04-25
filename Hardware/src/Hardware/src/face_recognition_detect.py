
import face_recognition
import cv2
import pickle
from picamera2 import Picamera2

class FaceRecognitionDetector:
    def __init__(self, encoding_file, webcam_index=0):
        self.encoding_file = encoding_file
        self.webcam_index = webcam_index
        self.known_face_encodings = []
        self.known_face_names = []
        self.cap = None
        self.picam = Picamera2()
        self.started = False

        # Load the pre-trained Haar Cascade classifier for face detection
        haarcascade_path = 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(haarcascade_path)

    def load_encodings(self):
        """Load known face encodings and names from a file."""
        try:
            with open(self.encoding_file, 'rb') as f:
                self.known_face_encodings, self.known_face_names = pickle.load(f)
            print(f"Loaded face encodings from {self.encoding_file}.")
        except FileNotFoundError:
            print(f"Error: The file {self.encoding_file} was not found.")
        except pickle.PickleError as e:
            print(f"Error loading face encodings: {e}")
            raise

    def start_webcam(self):
        """Initialize the webcam."""
        self.cap = cv2.VideoCapture(self.webcam_index)
        if not self.cap.isOpened():
            raise RuntimeError("Error: Could not open webcam.")
        print("Webcam initialized.")

    def stop_webcam(self):
        """Release the webcam and close any OpenCV windows."""
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Webcam released and OpenCV windows closed.")
    
    def get_frame_webcam(self):
        if self.started == True: 
            ret, frame = self.cap.read() 

        return frame
    
    def start_pi_camera(self): 
        # Configure the camera for still capture
        camera_config = self.picam.create_still_configuration(main={"size": (640, 480), "format": "RGB888"})
        self.picam.configure(camera_config)

        # Start the camerahaarcascade_frontalface_default.xml
        self.picam.start()
        self.started = True
        

    def stop_pi_camera(self): 
        if self.started == True: 
            self.picam.stop()
            self.picam.close()
            self.started = False
        

    def get_frame_pi(self):
        frame = self.picam.capture_array() 
        return frame
        
    def detect_face(self, frame):
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        return frame
        
    def detect_recognition(self, frame):
        """Process a single frame from the webcam."""
        # Convert the frame to RGB (face_recognition uses RGB format)
        
       # rgb_frame = frame[:, :, ::-1]
    
        # Find all the faces and face encodings in the frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        
        # Loop through each face in this frame of video
        for face_encoding in face_encodings:
            # Check if the face matches any known faces
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

            if True in matches:
                return True
            else:
                return False

# Usage example
if __name__ == '__main__':
    face = FaceRecognitionDetector('face_encodings.pkl')

    face.load_encodings() 

    face.start_pi_camera() 

    counter = 0 
    while True: 
        frame = face.get_frame_pi()

        face.detect_face(frame)

        cv2.imshow('Face Recognition', frame)

        if counter > 10:
            ret = face.detect_recognition(frame)
            counter = 0

            if ret == True: 
                print('Recognized!')
            else: 
                print('Nop')

        counter = counter + 1

        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break

    face.stop_pi_camera()
    cv2.destroyAllWindows()