
import time
import Adafruit_PCA9685
import RPi.GPIO as GPIO
import warnings
pwm = Adafruit_PCA9685.PCA9685()

#technical min-max is 68.25 - 409.5
#to reduce noise min-max will be considered 75 - 400	
min = 75
max = 400
neutral = 205
frequency = 33.33
pwm.set_pwm_freq(frequency)

	
def SetAngle(pin,angle,wait):
	#angle is odd due to the pulse width not being evenly distributed
	#	so it will be separated into many chunks with different math for each
	#	this isn't going to work well
	#Convering from degrees to microseconds
	if angle > 90 or angle < -90:
		warnings.warn("Out of range")
	elif angle <= -45:
		angle_convert = angle * -5.6
	elif angle >= 45:
		angle_convert = angle * 22
	elif angle < 0:
		angle_convert = angle * -14
	else
		angle_convert = angle * 20
	#converting from micrseconds to milliseconds
	angle_convert = angle_convert / 1000
	#convering to number of ticks for 12 bit 
	angle_convert = angle_convert / frequency * 4096
	pwm.set_pwm(pin,0,angle_convert)
	time.sleep(wait)

def SetMicros(pin,angle,wait)	
	if angle > 2100 or angle < 500:
		warnings.warn("Out of range")
	#converting from micrseconds to milliseconds
	angle_convert = angle / 1000
	#convering to number of ticks for 12 bit 
	angle_convert = angle_convert / frequency * 4096
	pwm.set_pwm(pin,0,angle_convert)
	time.sleep(wait)
	
def TiltUp(pin,wait):
	pwm.set_pwm(pin,0,max)
	time.sleep(wait)

def TiltDown(pin,wait):
	pwm.set_pwm(pin,0,min)
	time.sleep(wait)
	
def TiltMid(pin,wait):
	pwm.set_pwm(pin,0,neutral)
	time.sleep(wait)
	
def PanRight(pin,wait):
	pwm.set_pwm(pin,0,max)
	time.sleep(wait)
	
def PanLeft(pin,wait):
	pwm.set_pwm(pin,0,min)
	time.sleep(wait)
	
def PanMid(pin,wait):
	pwm.set_pwm(pin,0,neutral)
	time.sleep(wait)