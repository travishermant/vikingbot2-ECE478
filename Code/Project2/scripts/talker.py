#!/usr/bin/env python

import sys
#files related system 
sys.path.append("/home/pi/VikingBotFiles/Drivers/")

#packages related rospy
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
from time import sleep
import os

#handshaking signal which will indicate about recording signal
finishTalkPub = rospy.Publisher('TalkFinish', Int32, queue_size = 1)

def start_talking(data):
    fileName = data.data
    
    #command to do recording
    bashCommand = "aplay " + fileName
    os.system(bashCommand)
    
    #publish talking done
    finishTalkPub.publish(1)

def talker_node():
    rospy.init_node('talker_node')
    rospy.Subscriber('TalkCommand', String, start_talking)
    rospy.spin()

if __name__ == '__main__':
    print("ready for talking")
    try:
        talker_node()
    except rospy.ROSInterruptException():
        pass

