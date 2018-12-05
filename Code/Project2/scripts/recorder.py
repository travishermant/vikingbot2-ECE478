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

#keeps track of the recordings
recordCount = 0

#handshaking signal which will indicate about recording signal
finishRecordPub = rospy.Publisher('RecFinish', Int32, queue_size = 1)
recFilePub = rospy.Publisher('RecFinish', String, queue_size = 1)

def record(fileName, seconds):
    #command to do recording
    bashCommand = "arecord -D plughw:1,0 -d " + str(seconds) + " " + fileName
    os.system(bashCommand)

def do_record(data):
    global recordCount
    #FIXME for the path
    #should come from Constants
    path = "/home/pi/catkin_ws/src/project2/wav/"
    fileName = path + "microphone" + str(recordCount) + ".wav"

    rospy.loginfo(rospy.get_caller_id() + ' I heard %s', data.data)
    seconds = data.data
    
    #record the file
    record(fileName, seconds)
    recordCount = recordCount + 1
    
    #publish that you are done recording
    finishRecordPub.publish(1)
    #publish the name of the file
    recFilePub.publish(fileName)

def recorder_node():
    rospy.init_node('recorder_node')
    rospy.Subscriber('RecordCommand', Int32, do_record)
    rospy.spin()

if __name__ == '__main__':
    print("ready for recording")
    try:
        recorder_node()
    except rospy.ROSInterruptException():
        pass