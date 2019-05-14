# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import motion as motor

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

faceNeighborsMax = 2
neighborStep = 1

motor.RobotInit()
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    frame_h = image.shape[0] # frame_w = 640
    frame_w = image.shape[1] # frame_h = 480
    frameGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Perform multi scale detection of faces
    for neigh in range(1, faceNeighborsMax, neighborStep):
        #function whic detects an object
        #returns rectangles
        faces = faceCascade.detectMultiScale(frameGray, 1.2, neigh)
        frameClone = np.copy(image)
    
        # Display the image
        #for each rectangle detected
        for (x, y, w, h) in faces:
            #draw rectangle with red colour in clone image
            cv2.rectangle(frameClone, (x, y), (x + w, y + h), (255, 0, 0), 2)
            ####################################################
            # Draw a diagonal blue line with thickness of 5 px
            cv2.line(frameClone,(220, 0),(220, frame_h),(0,255,0),5) #green line
            cv2.line(frameClone,(320, 0),(320, frame_h),(0,0,255),5) #red line
            cv2.line(frameClone,(420, 0),(420, frame_h),(255,0,0),5) #blue line
                #print(' y + w/2 = %f'%(y+(w/2)))
                #print('w = %f'%w)
	        #print('h = %f'%h)
            if (220 <= (x + (w/2)) <= 420):
                print('stop')
                motor.RobotSTOP()
            elif ((x + (w/2)) < 220):
                print('turn left')
                motor.RobotLEFT()
            elif((x + (w/2)) > 420):
                print('turn right')
                motor.RobotRIGHT()
			
			
	#################################################
	# show the frame
    cv2.imshow("Frame", frameClone)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        motor.RobotDeInit()
        break
