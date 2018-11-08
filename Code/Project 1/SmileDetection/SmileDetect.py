# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

import Adafruit_PCA9685
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)

pwm = Adafruit_PCA9685.PCA9685()

frequency = 33.3

pwm.set_pwm_freq(frequency)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
facePath = "haarcascade_frontalface_default.xml"
smilePath = "haarcascade_smile.xml"
faceCascade = cv2.CascadeClassifier(facePath)
smileCascade = cv2.CascadeClassifier(smilePath)

pwm.set_pwm(12,0,190)
 

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    
    img = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale(gray,1.2,3)
    
    smileCount  = 0
    
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]

        smile = smileCascade.detectMultiScale(roi_gray,scaleFactor= 1.7,minNeighbors=17)

        
        # Set region of interest for smiles
        for (x, y, w, h) in smile:
            cv2.rectangle(roi_color, (x, y), (x+w, y+h), (255, 0, 0), 1)
            smileCount = smileCount + 1
    
    
    
    if(smileCount > 0):
        print("Smile")
        
        '''
        for i in range(3900,100,100):
            onTime = i
            offTime = 4096 - onTime
            pwm.set_pwm(12,onTime,offTime)
            time.sleep(0.5)
        
        onTime = 100
        offTime = 4096 - onTime
        pwm.set_pwm(12,onTime,offTime)
        time.sleep(1)
        
        for i in range(100,3900,100):            
            onTime = i 
            offTime = 4096 - onTime
            pwm.set_pwm(12,onTime,offTime)
            time.sleep(0.5)
        
        onTime = 3900 
        offTime = 4096 - onTime
        pwm.set_pwm(12,onTime,offTime)
        time.sleep(1)
        '''
        for i in range(191,241,1):
            pwm.set_pwm(12,0,i)
            time.sleep(0.01)
        time.sleep(1)
        for i in range(239,189,-1):
            pwm.set_pwm(12,0,i)
            time.sleep(0.01)
        time.sleep(1)
        '''
        pwm.set_pwm(12,0,240)
        time.sleep(1)
        pwm.set_pwm(12,0,190)
        time.sleep(1)
        '''
    #cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
cv2.destroyAllWindows()
GPIO.cleanup()