# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import BallDetectMove as bDM

#initalise GPIO for motion
bDM.RobotInit()

#some constants values
#get this value from trials
AREA_THRESHOLD = 18000
DISTANCE_THRESHOLD = 50
TIME_DIFFERENCE = 0.1

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)


#threshold values of color
#this is for red ball
#lightBallColor = (0, 108, 138)
#darkBallColor = (179, 223, 227)

#this is for orange ball
lightBallColor = (5, 114, 110)
darkBallColor = (11, 255, 247)

#this is for pink ball
#lightBallColor = (159, 109, 187)
#darkBallColor = (163, 135, 243)
	
#Read and display video frames until video is completed or 
#user quits by pressing ESC
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    '''
    frameR = frame.array
    output = frameR.copy()
    hsv_frame = cv2.cvtColor(frameR, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, lightBallColor, darkBallColor)
    mask = cv2.erode(mask, None, iterations=2)
    kernel = np.ones((9,9),np.uint8)
    mask = cv2.dilate(mask, None, iterations=2)
    
    output = cv2.bitwise_and(output, output, mask=mask)
    #output = cv2.dilate(output, None, iterations=2)
    #output = cv2.erode(output, None, iterations=2)
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    #_, binary = cv2.threshold(gray, 1, 255, cv2. THRESH_BINARY)
    #circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 3, 500, minRadius = 10, maxRadius = 200, param1 = 100, param2 = 70)
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 3, 500, minRadius = 10, maxRadius = 200, param1 = 100, param2 = 70)
    
    if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, radius) in circles:
                    cv2.circle(output, (x, y), radius, (0, 255, 0), 4)
    
    cv2.imshow("GRAY", gray)
    cv2.imshow("output", output)
    cv2.imshow("MASK", mask)
    '''
    
    frameR = frame.array
    output = frameR.copy()
    hsv_frame = cv2.cvtColor(frameR, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, lightBallColor, darkBallColor)
    
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #cv2.drawContours(frameR,contours,-1,(0,255,0), 3)
    
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    if(len(contour_sizes) > 0):
        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
        #cv2.drawContours(frameR,biggest_contour,-1,(0,255,0), 3)
        xR,yR,wR,hR = cv2.boundingRect(biggest_contour)
        #comment while deploying
        #cv2.rectangle(frameR,(xR,yR),(xR+wR,yR+hR),(0,255,0), 3)
        
        #add movement logic over here
        #calculate the X center
        #we dont care about the Y center
        detCenX = xR + wR/2
        #now lets see how far it is from center of camera
        diff = 320 - detCenX#FIXME get 320 from Constants
        #check whethere absolute value is whithin upper and lower bound
        absDiff = abs(diff)
        if(absDiff > DISTANCE_THRESHOLD):
            #check whether to take left or right
            if(diff > 0):
                bDM.RobotLEFT()
                time.sleep(TIME_DIFFERENCE)
                bDM.RobotSTOP()
            else:
                bDM.RobotRIGHT()
                time.sleep(TIME_DIFFERENCE)
                bDM.RobotSTOP()
        else:
            #calculate area
            areaOfBall = wR*hR
            #print(areaOfBall)
            #check whethere its below some thrshold or not
            if(areaOfBall < AREA_THRESHOLD):
                #move forward
                bDM.RobotFWD()
                time.sleep(TIME_DIFFERENCE)
                bDM.RobotSTOP()
            #else do nothing                    
    
    #comment while deploying
    #cv2.imshow("Cont", frameR)
    #cv2.imshow("MASK", mask) 
    
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    elif key == ord("s"):
        cv2.imwrite('BallImage.jpg',frameR)
    
		
# Closes all the frames
cv2.destroyAllWindows()
bDM.RobotDeInit()