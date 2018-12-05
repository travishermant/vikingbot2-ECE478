#!/usr/bin/env python

# Import Libraries 
import rospy
from random import randint
from std_msgs.msg import Int32
from std_msgs.msg import String
import time
import sys
import RPi.GPIO as GPIO

#switches on the H-bridge
L293E_IN1 = 21  
L293E_IN2 = 26
L293E_IN3 = 16
L293E_IN4 = 20
EN_1 = 13
EN_2 = 12
IR_PIN = 19

#defines for motion state publisher
STOP = 0
FORWARD = 1
LEFT = 2
RIGHT = 3
BACKWARD = 4

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

#create publishers
#this is useful for handshake purpose
pubRobotLocation = rospy.Publisher('/RobotState', Int32, queue_size=10)

#callback method for the motion command subscriber
def callback(data):
    motionCommand = data.data
    
    if(motionCommand == 'f'):
        print("forward")
        pubRobotLocation.publish(FORWARD)
        RobotFWD()
    elif (motionCommand == 'b'):
        print("back")
        pubRobotLocation.publish(BACKWARD)
        RobotBACK()
    elif (motionCommand == 'l'):
        print("left")
        pubRobotLocation.publish(LEFT)
        RobotLEFT()
    elif (motionCommand == 'r'):
        print("right")
        pubRobotLocation.publish(RIGHT)
        RobotRIGHT()
    elif (motionCommand == 's'):
        print("stop")
        pubRobotLocation.publish(STOP)
        RobotSTOP()
        
def motion_ros():
    print("in robot control")
    #initilize the node
    rospy.init_node("motion_ros", anonymous=True)
    #set the publishing rate
    rate = rospy.Rate(10) # 10Hz
        
    #create a subscriber for sensor values
    rospy.Subscriber("MotionCommand", String, callback)
    
    #publish motion_command values
    while not rospy.is_shutdown():
        #this will make sure we get scheduling for every 100 ms
        rate.sleep()
    rospy.spin()
        
if __name__ == '__main__':
    print("Ready to accept the command")
    
    #init GPIOS for robot
    RobotInit()
    GPIO.setup(IR_PIN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    try:
        motion_ros()
    except rospy.ROSInterruptException():
        pass
    #when ros exits
    #clean everything
    print("clean")
    RobotDeInit()