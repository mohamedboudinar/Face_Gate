import os
import face_recognition
import pickle

class FaceRecognitionTrainer:
    def __init__(self, image_dir , encoding_file):
        self.image_dir = image_dir
        self.encoding_file = encoding_file
        self.known_face_encodings = []
        self.known_face_names = []

    def __str__(self):
        """Return a string representation of the instance."""
        return (f"FaceRecognitionTrainer(image_dir={self.image_dir}, "
                f"encoding_file={self.encoding_file})")

    def load_and_train_images(self):
        """Load images from the directory and train face recognition model."""
        for filename in os.listdir(self.image_dir):
            if filename.endswith(".jpg"):
                img_path = os.path.join(self.image_dir, filename)
                image = face_recognition.load_image_file(img_path)
                face_encodings = face_recognition.face_encodings(image)

                if face_encodings:
                    self.known_face_encodings.append(face_encodings[0])
                    self.known_face_names.append("Known Person")

        print("Training complete.")

    def save_encodings(self):
        """Save the face encodings and names to a file."""
        with open(self.encoding_file, 'wb') as f:
            pickle.dump((self.known_face_encodings, self.known_face_names), f)
        print(f"Encodings saved to {self.encoding_file}.")


# Usage example
if __name__ == '__main__':
    train = FaceRecognitionTrainer('received_images/ras_zebi', 'face_encodings.pkl')
    train.load_and_train_images()
    train.save_encodings()