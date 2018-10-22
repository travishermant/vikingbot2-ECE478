import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
#switches on the H-bridge
L293E_IN1=21  
L293E_IN2=20
L293E_IN3=16
L293E_IN4=26

#initializing GPIO pins to low outputs 
GPIO.setup(L293E_IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(L293E_IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(L293E_IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(L293E_IN4,GPIO.OUT,initial=GPIO.LOW)

#movement logic
def RobotFWD():
	GPIO.output(L293E_IN1,True)
	GPIO.output(L293E_IN2,False)
	GPIO.output(L293E_IN3,True)
	GPIO.output(L293E_IN4,False)

def RobotRIGHT():
	GPIO.output(L293E_IN1,False)
	GPIO.output(L293E_IN2,True)
	GPIO.output(L293E_IN3,True)
	GPIO.output(L293E_IN4,False)

def RobotLEFT():
	GPIO.output(L293E_IN1,True)
	GPIO.output(L293E_IN2,False)
	GPIO.output(L293E_IN3,False)
	GPIO.output(L293E_IN4,True)

def RobotBACK():
	GPIO.output(L293E_IN1,False)
	GPIO.output(L293E_IN2,True)
	GPIO.output(L293E_IN3,False)
	GPIO.output(L293E_IN4,True)

def RobotSTOP():
	GPIO.output(L293E_IN1,False)
	GPIO.output(L293E_IN2,False)
	GPIO.output(L293E_IN3,False)
	GPIO.output(L293E_IN4,False)


while True:
	try:
		x = raw_input("Enter the command")
		print(x)
		if(x == '1'):
			RobotFWD()
		elif (x == '2'):
			RobotLEFT()
		elif (x == '3'):
			RobotRIGHT()
		elif (x == '4'):
			RobotBACK()
		else:
			RobotSTOP()
		# time.sleep(1);
	except KeyboardInterrupt:
		break
		
GPIO.cleanup()