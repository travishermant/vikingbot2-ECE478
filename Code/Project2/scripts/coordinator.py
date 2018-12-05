#!/usr/bin/env python

#this is going to be the coordinator
#which will have state machine
#main state will be whether to be in a thetre mode
#or command mode
#attime of command mode recording will go on
#at time of thetre mode we will stop the recording
#the coordinator will also communicate with other robot
#and keep track of all the handshakings

#other approach can be circuit programming approach like HAL of linuxcnc
#where topics are directly connected like hal pins

import sys
#files related system 
sys.path.append("/home/pi/VikingBotFiles/Drivers/")

#packages related rospy
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
from time import sleep
import os

#FIXME
#get this from constants
#name of the files to be played
forwardAudio = '/home/pi/catkin_ws/src/project2/wav/1.mp3'
backwardAudio = '/home/pi/catkin_ws/src/project2/wav/2.mp3'
leftAudio = '/home/pi/catkin_ws/src/project2/wav/3.mp3'
rightAudio = '/home/pi/catkin_ws/src/project2/wav/4.mp3'


recCommandPub = rospy.Publisher('RecordCommand', Int32, queue_size = 1)
speechRecCommandPub = rospy.Publisher('RecogniseCommand', String, queue_size = 1)
motCommandPub = rospy.Publisher('MotionCommand', String, queue_size = 1)
talkCommandPub = rospy.Publisher('TalkCommand', String, queue_size = 1)

#Main states
COMMAND_MODE = 0
PLAY_MODE = 100

#command states
CM_RESET=0
CM_SEND_RECORDING = 1
CM_WAIT_FOR_RECORDING=2
CM_SEND_TO_DF=3
CM_WAIT_FOR_DF=4
CM_SEND_MOTION=5
CM_WAIT_FOR_MOTION=6
CM_SEND_TALK=7
CM_WAIT_FOR_TALK=8
CM_IDLE=9
CM_ERROR=10

#state variable for main state machine
state = COMMAND_MODE
prevState = COMMAND_MODE

#state variable for command state machine
#FIXME can we do something better
#like separating the state machines in different file or rosrun
cState = CM_RESET


#some hand shaking variables
recordRequest = 0;
recogniseRequest = 0;
motionRequest = 0;
motionCommandToExecute = 0;
lastRecordedFile = ''

def talk_done(data):
    pass

def recording_done(data):
    pass

def save_name_of_file(data):
    global lastRecordedFile;
    global recordRequest;
    
    lastRecordedFile = data.data
    print('Recorded '+lastRecordedFile)
    
    if(recordRequest == 0):
        recordRequest = 1

def robot_state_change(data):
    pass

def robot_motion_done(data):
    global motionRequest;
    if(motionRequest == 0):
        motionRequest = 1

def df_recv_string(data):
    global recogniseRequest
    global motionCommandToExecute
    global motionCommandFound
    if(recogniseRequest == 0):
        recogniseRequest = 1
        print(data.data)
        recvStr = data.data
        #check for the motion commands
        if(recvStr.find('forward') >= 0):
            motionCommandFound = 1
            motionCommandToExecute = 1
        elif(recvStr.find('left') >= 0):
            motionCommandFound = 1
            motionCommandToExecute = 2
        elif(recvStr.find('right') >= 0):
            motionCommandFound = 1
            motionCommandToExecute = 3
        elif(recvStr.find('back') >= 0):
            motionCommandFound = 1
            motionCommandToExecute = 4
        else:
            motionCommandFound = 0
            motionCommandToExecute = 0

def coordinator_node():
    global recordRequest;
    global lastRecordedFile;
    global recogniseRequest;
    global motionRequest;
    global motionCommandFound;
    global motionCommandToExecute;
    global state,prevState;
    global cState;
    rospy.init_node('coordinator_node')
    rospy.Subscriber('TalkFinish', Int32, talk_done)
    rospy.Subscriber('RecFinish', Int32, recording_done)
    rospy.Subscriber('RecFilePath', String, save_name_of_file)
    rospy.Subscriber('RobotState', Int32, robot_state_change)
    rospy.Subscriber('RobotMotionDone', Int32, robot_motion_done)
    
    rospy.Subscriber('SpeechRecString', String, df_recv_string)
    
    #set the servo thread rate
    #100 ms is fair enough time
    rate = rospy.Rate(10) # 10Hz
    
    while not rospy.is_shutdown():
        
        #state machine logic
        if(state == COMMAND_MODE):
            #state machine of command mode
            if(cState == CM_RESET):
                cState = CM_SEND_RECORDING
            elif(cState == CM_SEND_RECORDING):
                #put this flag to
                recordRequest = 0
                #publish the topic to start recording for 4 seconds
                recCommandPub.publish(5)
                cState = CM_WAIT_FOR_RECORDING
            elif(cState == CM_WAIT_FOR_RECORDING):
                if(recordRequest == 1):
                    cState = CM_SEND_TO_DF
            elif(cState == CM_SEND_TO_DF):
                recogniseRequest = 0
                speechRecCommandPub.publish(lastRecordedFile)
                cState = CM_WAIT_FOR_DF
            elif(cState == CM_WAIT_FOR_DF):
                if(recogniseRequest == 1):
                    #now go back to reset state
                    #add code of motion over here
                    if(motionCommandFound == 1):
                        motionCommandFound = 0
                        cState = CM_SEND_MOTION
                    else:
                        cState = CM_SEND_RECORDING
            elif(cState == CM_SEND_MOTION):
                if(motionCommandToExecute == 1):
                    motionRequest = 0
                    motCommandPub.publish("fs")
                    cState = CM_WAIT_FOR_MOTION
                elif(motionCommandToExecute == 2):
                    motionRequest = 0
                    motCommandPub.publish("ls")
                    cState = CM_WAIT_FOR_MOTION
                elif(motionCommandToExecute == 3):
                    motionRequest = 0
                    motCommandPub.publish("rs")
                    cState = CM_WAIT_FOR_MOTION
                elif(motionCommandToExecute == 4):
                    motionRequest = 0
                    motCommandPub.publish("bs")
                    cState = CM_WAIT_FOR_MOTION                
                else:
                    cState = CM_SEND_RECORDING
            elif(cState == CM_WAIT_FOR_MOTION):
                if(motionRequest == 1):
                    cState = CM_SEND_RECORDING
            elif(cState == CM_IDLE):
                pass
                                    
        elif(state == PLAY_MODE):
            #add play state machine over here
            pass
        else:
            #should never come over here
            print("Something is wrong here")
        
        #this will make sure we get scheduling for every 100 ms
        rate.sleep()
    
    rospy.spin()

if __name__ == '__main__':
    print("ready for coordinating")
    try:
        coordinator_node()
    except rospy.ROSInterruptException():
        pass