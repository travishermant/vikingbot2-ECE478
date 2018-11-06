#In the following code, we will use the VideoCapture Object 
#to read a video file and display it.
# Import OpenCV and numpy
import cv2
import numpy as np

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
# cap = cv2.VideoCapture('chaplin.mp4')
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if (cap.isOpened()== False): 
	print("Error opening video stream or file")

#threshold values of color
lightBallColor = (2, 90, 10)
darkBallColor = (38, 175, 255)
	
#Read and display video frames until video is completed or 
#user quits by pressing ESC
while(cap.isOpened()):
# Capture frame-by-frame
	ret, frame = cap.read()
	if ret == True:
		'''
		# Covert color space to HSV as it is much easier to filter colors in the HSV color-space.
		hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		blur = cv2.GaussianBlur(hsv_frame,(11,11),0)
		
		mask = cv2.inRange(blur, lightBallColor, darkBallColor)
		
		# Taking a matrix of size 5 as the kernel 
		# kernel = np.ones((9,9), np.uint8) 
		# img_dilation = cv2.dilate(mask, kernel, iterations=1) 
		
		circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
		
		try:
			circles = np.uint16(np.around(circles))
			
			for i in circles[0,:]:
				# draw the outer circle
				cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
				# draw the center of the circle
				cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
		except:
			pass
		
		# Display the resulting frame
		cv2.imshow('Frame',frame)
		# cv2.imshow('HSV Frame',hsv_frame)
		# cv2.imshow('Result ',mask)
		cv2.imshow('Blur Result Dia',mask)
		'''
		output = frame.copy()
		hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv_frame, lightBallColor, darkBallColor)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		
		output = cv2.bitwise_and(output, output, mask=mask)
		#output = cv2.dilate(output, None, iterations=2)
		#output = cv2.erode(output, None, iterations=2)
		gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
		#_, binary = cv2.threshold(gray, 1, 255, cv2. THRESH_BINARY)
		circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 3, 500, minRadius = 10, maxRadius = 200, param1 = 100, param2 = 60)
		
		if circles is not None:
			circles = np.round(circles[0, :]).astype("int")
			for (x, y, radius) in circles:
				cv2.circle(output, (x, y), radius, (0, 255, 0), 4)
				
		cv2.imshow("output", output)
	else:
		break;
		
	# Press esc on keyboard to  exit
	key = cv2.waitKey(25) & 0xFF
	if key == 27:
		break
	elif (key == ord('c')):
		cv2.imwrite('BallImage.jpg',frame)
		
# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()