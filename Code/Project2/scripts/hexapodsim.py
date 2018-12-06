#!/usr/bin/env python

import os

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
from time import sleep

#two pulisheres for handshaking with our robot
playSeqStarted = rospy.Publisher('PlaySeqStarted', Int32, queue_size = 1)
nextPlaySeq = rospy.Publisher('NextPlaySeq', Int32, queue_size = 1)

seqCounter = 0

def start_play(data):
    global seqCounter
    print('starting play')
    seqCounter = 0
    playSeqStarted.publish(1)

def do_some_task_and_reply(data):
    global seqCounter
    #can be useful for indexing
    #of audio files for sim purpose
    seqCounter = seqCounter + 1
    sleep(3)
    nextPlaySeq.publish(1)

def hexapodsim_node():
    rospy.init_node('hexapodsim_node')
    rospy.Subscriber('PlaySeqStartReq', Int32, start_play)
    rospy.Subscriber('NextPlaySeqReq', Int32, do_some_task_and_reply)
    rospy.spin()

if __name__ == '__main__':
    print("ready for simulation")
    try:
        hexapodsim_node()
    except rospy.ROSInterruptException():
        pass
