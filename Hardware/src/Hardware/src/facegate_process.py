from face_recognition_train import FaceRecognitionTrainer
from face_recognition_server import ImageReceiverServer
from face_recognition_detect import FaceRecognitionDetector
import threading 
import time 
import cv2
from lcd import LcdProcess

PATH_OUT_IMAGES_SERV="/home/admin/Hardware/received_images"
PATH_OUT_IMAGES_TRAIN="/home/admin/Hardware/received_images/ines"
PATH_OUT_TRAINED_DATA="/home/admin/Hardware/train_data/face_encodings.pkl"
HOST_IP= "0.0.0.0" 
HOST_PORT=4899

UNKNOWN = 0
CHECKED_IN=1
CHECKED_OUT=2

class FaceGateProcessor:

    def __init__(self):
        self.condition = threading.Condition()
        self.flag = threading.Event()
        self.data_ready = False
        self.send_sig = False
        self.sig_type = False

        self.facegate_trainer = FaceRecognitionTrainer(image_dir=PATH_OUT_IMAGES_TRAIN , encoding_file=PATH_OUT_TRAINED_DATA)
        self.facegate_server = ImageReceiverServer(host=HOST_IP, port=HOST_PORT, save_base_folder=PATH_OUT_IMAGES_SERV)
        self.facegate_detection = FaceRecognitionDetector(encoding_file=PATH_OUT_TRAINED_DATA, webcam_index=0)
        self.__lcd = LcdProcess()

    def process_hardware(self):
        # Include Hardware here
        
        self.facegate_detection.load_encodings()
        self.facegate_detection.start_pi_camera() 

        load_counter = 0
        process_counter = 0

        recognized = False
        sendSignal = False
        faceProcess = False
        action = UNKNOWN

        
        self.__lcd.show_main_menu()

        while True:
            if self.flag.is_set():
                print("Loading encoding for face recognition")
                self.facegate_detection.load_encodings()
                self.flag.clear()            
            
            if self.__lcd.check_button_check_in() == 1: 
                print('Starting Face Process for Check in')
                faceProcess = True
                action = CHECKED_IN
            elif self.__lcd.check_button_check_out() == 1: 
                print('Starting Face Process for Checkout')
                faceProcess = True 
                action = CHECKED_OUT
            else: 
                if faceProcess == False: 
                    self.__lcd.show_main_menu()

            if faceProcess == True:
                
                print('Started Face Process')

                frame = self.facegate_detection.get_frame_pi()

                self.facegate_detection.detect_face(frame)

                cv2.imshow('Face Recognition', frame)
                load_counter = load_counter + 1

                k = cv2.waitKey(30) & 0xff
                if k == 27: # press 'ESC' to quit
                    break

                if load_counter > 5:
                    print('Recognition...')
                    recognized = self.facegate_detection.detect_recognition(frame)
                    process_counter = process_counter + 1 
                    if process_counter > 10:
                        print('Recognition Done...')
                        process_counter = 0
                        load_counter = 0
                        faceProcess = False
                        sendSignal = True
                        cv2.destroyAllWindows()

            if sendSignal == True: 
                print('Sending Signals')
                if recognized == True: 
                    if action == CHECKED_IN:
                        self.__lcd.show_check_in_menu()
                    elif action == CHECKED_OUT: 
                        self.__lcd.show_out_menu()
                    else:
                        pass

                    print('Recognized...')
                    self.send_sig = True
                    self.sig_type = True 
                    time.sleep(5)
                    sendSignal = False 
                else:
                    print('Not Recognized...')
                    self.__lcd.show_rejected_menu()
                    self.send_sig = True
                    self.sig_type = False
                    time.sleep(5)
                    sendSignal = False

    def process_server(self):

        while True:
            with self.condition:
                self.facegate_server.start_server()
                print("Server: Data received...")
                self.data_ready = True
                
                self.condition.notify()
                
                # Wait until data is processed
                while self.data_ready:
                    self.condition.wait()
                

    def process_train(self):

        while True:
            with self.condition:
                print("Processor: Waiting for a signal...")
                while not self.data_ready:
                    self.condition.wait()
                
                # Process the data
                print("Processor: Signal received, processing data...")
                self.facegate_trainer.load_and_train_images()
                self.facegate_trainer.save_encodings()
                
                # Mark data as processed
                self.data_ready = False
                self.flag.set()
                self.condition.notify()


    def run(self): 
        server_thread = threading.Thread(target=self.process_server)
        train_thread = threading.Thread(target=self.process_train)
        hardware_thread = threading.Thread(target=self.process_hardware)

        server_thread.start()
        train_thread.start()
        hardware_thread.start()

        server_thread.join()
        train_thread.join()
        hardware_thread.join()
