import time
import RPi.GPIO as GPIO


#switches on the H-bridge
L293E_IN1 = 21  
L293E_IN2 = 26
L293E_IN3 = 16
L293E_IN4 = 20
EN_1 = 13
EN_2 = 12

def RobotInit():
    GPIO.setmode(GPIO.BCM)
    #initializing GPIO pins to low outputs 
    GPIO.setup(L293E_IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(L293E_IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(L293E_IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(L293E_IN4,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(EN_1,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(EN_2,GPIO.OUT,initial=GPIO.HIGH)

#movement logic
def RobotFWD():
	GPIO.output(L293E_IN1,False)
	GPIO.output(L293E_IN2,True)
	GPIO.output(L293E_IN3,False)
	GPIO.output(L293E_IN4,True)
    
def RobotBACK():
	GPIO.output(L293E_IN1,True)
	GPIO.output(L293E_IN2,False)
	GPIO.output(L293E_IN3,True)
	GPIO.output(L293E_IN4,False)

def RobotLEFT():
	GPIO.output(L293E_IN1,False)
	GPIO.output(L293E_IN2,True)
	GPIO.output(L293E_IN3,True)
	GPIO.output(L293E_IN4,False)

def RobotRIGHT():
	GPIO.output(L293E_IN1,True)
	GPIO.output(L293E_IN2,False)
	GPIO.output(L293E_IN3,False)
	GPIO.output(L293E_IN4,True)
	
def RobotSTOP():
	GPIO.output(L293E_IN1,False)
	GPIO.output(L293E_IN2,False)
	GPIO.output(L293E_IN3,False)
	GPIO.output(L293E_IN4,False)

def RobotDeInit():
    GPIO.cleanup()