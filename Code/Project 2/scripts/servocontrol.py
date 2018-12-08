#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
from time import sleep
import os
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

frequency = 33.3

pwm.set_pwm_freq(frequency)

pwm.set_pwm(12,0,190)

servoDone = rospy.Publisher('ServoMotDone', Int32, queue_size = 1)

def do_nod(data):
    for i in range(191,241,1):
        pwm.set_pwm(12,0,i)
        sleep(0.01)
    sleep(1)
    for i in range(239,189,-1):
        pwm.set_pwm(12,0,i)
        sleep(0.01)
    sleep(1)
    servoDone.publish(1);

def servocontrol_node():
    rospy.init_node('servocontrol_node')
    rospy.Subscriber('ServoCommand', Int32, do_nod)
    rospy.spin()

if __name__ == '__main__':
    print("ready for servo control")
    try:
        servocontrol_node()
    except rospy.ROSInterruptException():
        pass