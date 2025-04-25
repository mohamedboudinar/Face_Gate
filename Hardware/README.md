# ines-project



## Installation 

RPI.GPIO Librarby must be installed, check link in Documentation. \
LCD Display lib must be installed \
pip install ST7735 \ 
PIL must be installed


## Documentation 

The Hardware Layer is not from scratch.\
using the RPI Gpio BCM Layer:\
https://pythonhosted.org/RPIO/


## Module - Deployment phase 

### Display
lcd_config.py: Contains the gpio and spi setup for the raspi hardware. In this class the SPI and also 8 INPUT buttons (Keypads and Keys) parameters will be initialised using the official gpiozero and spidev packages. The lcd_config is a library written by wireshark.\
lcd_driver.py: Is the class that implements the spi communication protocoll between the raspberry pi and the wireshark lcd display. The lcd_driver is a library written by wireshark.\
lcd.py: Implements the lcd_config and lcd_display packages for application purposes. This Class will show diffent Texts like Check in and out and will be used as a trigger to the image processing process.


### Stepper Motor

stepper_motor.py: Is a simple class that uses RPi.GPIO to controll the stepper motor in both directions with different speed parameters.

### Camera 

camera_interr.py: a simple class that uses PiCamera2 package to communicate with the RPi CAM 3 Camera and get frames. as a test programm these frames will be streamed as a video using OpenCV. 




## TODOs - Futur implementation

main.py: will call the main process of the application.\
face_recognition_server.py: This class will communicate with the client using the Socket package. localhost ip (127.0.0.1) will be used to send signals and data.\
On trigger from the client, the client will send 10 pictures of the person to be registered as a known face and also the name of the person. The data will be then stored on the ROM of the Raspberry Pi.\
face_recognition_mod.py: This class will use the face recognition package and will read and process the received images. With the help of the 10 images the model will learn and will detect the saved face.\
image_processing.py: will get the frames from the camera_interr.py class and will process them to detect the face of the person in front of the camera.


## Use-Case/Process

1 - The client (website) will trigger the face_recgonition_server process.\
2 - Using localhost ip (ethernet communication) the pictures and informations of the person will be sent.\ 
3 - The Images and informations will be saved in ROM.\ 
4 - The Face Recognition model will be activated and will learn the model using the received images.\
5 - The model has saved a new person.\ 
6 - The user will on the display button for check in.\
7 - Image processing will start.\
8 - Face will be detected and compared with the saved known_hosts from face recognition.\
9 - If the Face meets the criteria - Approval will be sent to the client.\
10 - The Client will save the check in time stamp.\
11 - The Hardware will be controller moving the stepper motor to open the door.\
12 - After 10 s the door will close.\
13 - Process will be repeated for check out.\
14 - Client will calculate the worked hours : (Checkout - Checkin) - Pause


## Running Tests.

1 - Navigate to the project: cd ~/ines-project (recheck hierarchie with ls and renavigate with cd).\
2 - Run motor: ./run_motor.sh \
3 - RUn Lcd: ./run_lcd.sh \
4 - Run Camera: ./run_camera.sh \
5 - Process can be interrupted by Ctrl + C.