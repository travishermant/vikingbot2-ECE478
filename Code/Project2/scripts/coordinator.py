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

playSeqStartReqPub = rospy.Publisher('PlaySeqStartReq', Int32, queue_size = 1)
nextPlaySeqReqPub = rospy.Publisher('NextPlaySeqReq', Int32, queue_size = 1)
servoCommandReq = rospy.Publisher('ServoCommand', Int32, queue_size = 1)

tTSReqPub = rospy.Publisher('TTSReq', String, queue_size = 1)

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
CM_SEND_TO_POLLY=11
CM_WAIT_FOR_POLLY=12

#play mode states
PM_RESET=0
PM_START_PLAY=1
PM_WAIT_FOR_STARTED=2

PM_SEQ_1_TALK=3
PM_SEQ_1_TALK_WAIT=4

PM_SEQ_1_MOTION=5
PM_SEQ_1_MOTION_WAIT=6

PM_SEQ_1_MOTION_1=7
PM_SEQ_1_MOTION_WAIT_1=8

PM_SEQ_1_SEND=9
PM_SEQ_1_SEND_WAIT=10

PM_SEQ_2_TALK=11
PM_SEQ_2_TALK_WAIT=12

PM_SEQ_2_MOTION=13
PM_SEQ_2_MOTION_WAIT=14

PM_SEQ_2_MOTION_1=15
PM_SEQ_2_MOTION_WAIT_1=16

PM_SEQ_2_SEND=17
PM_SEQ_2_SEND_WAIT=18

PM_SEQ_3_TALK=19
PM_SEQ_3_TALK_WAIT=20

PM_SEQ_3_MOTION=21
PM_SEQ_3_MOTION_WAIT=22

PM_SEQ_3_MOTION_1=23
PM_SEQ_3_MOTION_WAIT_1=24

PM_SEQ_3_SEND=25
PM_SEQ_3_SEND_WAIT=26

PM_SEQ_4_TALK=27
PM_SEQ_4_TALK_WAIT=28

PM_SEQ_4_MOTION=29
PM_SEQ_4_MOTION_WAIT=30

PM_SEQ_4_MOTION_1=31
PM_SEQ_4_MOTION_WAIT_1=32

PM_SEQ_4_SEND=33
PM_SEQ_4_SEND_WAIT=34

PM_DONE=100

#state variable for main state machine
state = COMMAND_MODE
prevState = COMMAND_MODE

#state variable for command state machine
#FIXME can we do something better
#like separating the state machines in different file or rosrun
cState = CM_RESET

#state variable for play mode i.e. thetre mode
pState = PM_RESET

#han shaking signals for play sequesnce
playStartReq = 0
nextSeqReq = 0



#some hand shaking variables
recordRequest = 0;
recogniseRequest = 0;
motionRequest = 0;
talkReq = 0
servoMoveReq = 0
tTSReq = 0

#variable which tells which motion command i want to execute
#depends upon dialogflow response
motionCommandToExecute = 0;
lastRecordedFile = ''
diaResponse = ''


def talk_done(data):
    global talkReq
    if(talkReq == 0):
        talkReq = 1

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
    global diaResponse
    diaResponse = data.data
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
        elif(recvStr.find('theater') >= 0):
            motionCommandFound = 1
            motionCommandToExecute = 6
        else:
            motionCommandFound = 0
            motionCommandToExecute = 0
            
def play_has_started(data):
    global playStartReq
    if playStartReq == 0:
        playStartReq = 1

def execute_next_sequence(data):
    global nextSeqReq
    if nextSeqReq == 0:
        nextSeqReq = 1
   
def servo_movement_done(data):
    global servoMoveReq
    if(servoMoveReq == 0):
        servoMoveReq = 1
        
def tts_done(data):
    global tTSReq
    if(tTSReq == 0):
        tTSReq = 1

def coordinator_node():
    global recordRequest;
    global lastRecordedFile;
    global recogniseRequest;
    global talkReq;
    global motionRequest;
    global motionCommandFound;
    global motionCommandToExecute;
    global playStartReq
    global nextSeqReq
    global servoMoveReq
    global tTSReq
    global state,prevState;
    global cState;
    global pState
    global diaResponse
    rospy.init_node('coordinator_node')
    rospy.Subscriber('TalkFinish', Int32, talk_done)
    rospy.Subscriber('RecFinish', Int32, recording_done)
    rospy.Subscriber('RecFilePath', String, save_name_of_file)
    rospy.Subscriber('RobotState', Int32, robot_state_change)
    rospy.Subscriber('RobotMotionDone', Int32, robot_motion_done)
    
    rospy.Subscriber('SpeechRecString', String, df_recv_string)
    
    rospy.Subscriber('PlaySeqStarted', Int32, play_has_started)
    rospy.Subscriber('NextPlaySeq', Int32, execute_next_sequence)
    
    rospy.Subscriber('ServoMotDone', Int32, servo_movement_done)
    
    rospy.Subscriber('TTSDone', Int32, tts_done)
    
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
                    #delete the file
                    #so it doesnt overflow the memory
                    os.remove(lastRecordedFile)
                    #check if not null
                    if(diaResponse != ''):
                        cState = CM_SEND_TO_POLLY
                    else:
                        cState = CM_SEND_RECORDING
            elif(cState == CM_SEND_TO_POLLY):
                tTSReq = 0
                cState = CM_WAIT_FOR_POLLY
                tTSReqPub.publish(diaResponse)
            elif(cState == CM_WAIT_FOR_POLLY):
                if(tTSReq == 1):
                    cState = CM_SEND_TALK
            elif(cState == CM_SEND_TALK):        
                talkReq = 0  
                talkCommandPub.publish('/home/pi/catkin_ws/src/project2/wav/speech.mp3')    
                cState = CM_WAIT_FOR_TALK   
            elif(cState == CM_WAIT_FOR_TALK):
                if(talkReq == 1):
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
                elif(motionCommandToExecute == 6):
                    #go to idle state
                    #from there play state machine will take over
                    cState = CM_IDLE
                else:
                    cState = CM_SEND_RECORDING
            elif(cState == CM_WAIT_FOR_MOTION):
                if(motionRequest == 1):
                    cState = CM_SEND_RECORDING
            elif(cState == CM_IDLE):
                state = PLAY_MODE
                cState = CM_RESET
                pState = PM_RESET
                                    
        elif(state == PLAY_MODE):
            #add play state machine over here
            if(pState == PM_RESET):
                pState = PM_START_PLAY
            elif(pState == PM_START_PLAY):
                playStartReq = 0
                pState = PM_WAIT_FOR_STARTED
                playSeqStartReqPub.publish(1)
            elif(pState == PM_WAIT_FOR_STARTED):
                if(playStartReq == 1):
                    pState = PM_SEQ_1_TALK
            elif(pState == PM_SEQ_1_TALK):
                talkReq = 0
                pState = PM_SEQ_1_TALK_WAIT
                talkCommandPub.publish('/home/pi/catkin_ws/src/project2/wav/1.mp3')
            elif(pState == PM_SEQ_1_TALK_WAIT):
                if(talkReq == 1):
                    pState = PM_SEQ_1_MOTION    
            elif(pState == PM_SEQ_1_MOTION):
                #turnleft
                motionRequest = 0
                motCommandPub.publish("ls")
                pState = PM_SEQ_1_MOTION_WAIT
            elif(pState == PM_SEQ_1_MOTION_WAIT):    
                if(motionRequest == 1):
                    pState = PM_SEQ_1_MOTION_1    
            elif(pState == PM_SEQ_1_MOTION_1):
                #move head
                servoMoveReq = 0
                servoCommandReq.publish(1)
                pState = PM_SEQ_1_MOTION_WAIT_1    
            elif(pState == PM_SEQ_1_MOTION_WAIT_1):
                if(servoMoveReq == 1):
                    pState = PM_SEQ_1_SEND
            elif(pState == PM_SEQ_1_SEND):
                pState = PM_SEQ_1_SEND_WAIT
                nextSeqReq = 0
                nextPlaySeqReqPub.publish(1)
            elif(pState == PM_SEQ_1_SEND_WAIT):
                if(nextSeqReq == 1):
                    pState = PM_SEQ_2_TALK
            elif(pState == PM_SEQ_2_TALK):        
                talkReq = 0
                pState = PM_SEQ_2_TALK_WAIT
                talkCommandPub.publish('/home/pi/catkin_ws/src/project2/wav/2.mp3')
            elif(pState == PM_SEQ_2_TALK_WAIT):
                if(talkReq == 1):
                    pState = PM_SEQ_2_MOTION
            elif(pState == PM_SEQ_2_MOTION):        
                #turnleft
                motionRequest = 0
                motCommandPub.publish("ls")
                pState = PM_SEQ_2_MOTION_WAIT
            elif(pState == PM_SEQ_2_MOTION_WAIT):
                if(motionRequest == 1):
                    pState = PM_SEQ_2_MOTION_1    
            elif(pState == PM_SEQ_2_MOTION_1):    
                #turn right
                motionRequest = 0
                motCommandPub.publish("rs")
                pState = PM_SEQ_2_MOTION_WAIT_1
            elif(pState == PM_SEQ_2_MOTION_WAIT_1):
                if(motionRequest == 1):
                    pState = PM_SEQ_2_SEND
            elif(pState == PM_SEQ_2_SEND):
                pState = PM_SEQ_2_SEND_WAIT
                nextSeqReq = 0
                nextPlaySeqReqPub.publish(1)
            elif(pState == PM_SEQ_2_SEND_WAIT):
                if(nextSeqReq == 1):
                    pState = PM_SEQ_3_TALK
                    
            elif(pState == PM_SEQ_3_TALK):        
                talkReq = 0
                pState = PM_SEQ_3_TALK_WAIT
                talkCommandPub.publish('/home/pi/catkin_ws/src/project2/wav/3.mp3')
            elif(pState == PM_SEQ_3_TALK_WAIT):
                if(talkReq == 1):
                    pState = PM_SEQ_3_MOTION
            elif(pState == PM_SEQ_3_MOTION):        
                #turnright
                motionRequest = 0
                motCommandPub.publish("rs")
                pState = PM_SEQ_3_MOTION_WAIT
            elif(pState == PM_SEQ_3_MOTION_WAIT):
                if(motionRequest == 1):
                    pState = PM_SEQ_3_MOTION_1    
            elif(pState == PM_SEQ_3_MOTION_1):    
                #turn left
                motionRequest = 0
                motCommandPub.publish("ls")
                pState = PM_SEQ_3_MOTION_WAIT_1
            elif(pState == PM_SEQ_3_MOTION_WAIT_1):
                if(motionRequest == 1):
                    pState = PM_SEQ_3_SEND
            elif(pState == PM_SEQ_3_SEND):
                pState = PM_SEQ_3_SEND_WAIT
                nextSeqReq = 0
                nextPlaySeqReqPub.publish(1)
            elif(pState == PM_SEQ_3_SEND_WAIT):
                if(nextSeqReq == 1):
                    pState = PM_SEQ_4_TALK
                    
            elif(pState == PM_SEQ_4_TALK):        
                talkReq = 0
                pState = PM_SEQ_4_TALK_WAIT
                talkCommandPub.publish('/home/pi/catkin_ws/src/project2/wav/4.mp3')
            elif(pState == PM_SEQ_4_TALK_WAIT):
                if(talkReq == 1):
                    pState = PM_SEQ_4_MOTION
            elif(pState == PM_SEQ_4_MOTION):        
                #nod
                servoMoveReq = 0
                servoCommandReq.publish(1)
                pState = PM_SEQ_4_MOTION_WAIT
            elif(pState == PM_SEQ_4_MOTION_WAIT):
                if(servoMoveReq == 1):
                    pState = PM_SEQ_4_MOTION_1    
            elif(pState == PM_SEQ_4_MOTION_1):    
                #move forward
                motionRequest = 0
                motCommandPub.publish("fs")
                pState = PM_SEQ_4_MOTION_WAIT_1
            elif(pState == PM_SEQ_4_MOTION_WAIT_1):
                if(motionRequest == 1):
                    pState = PM_SEQ_4_SEND
            elif(pState == PM_SEQ_4_SEND):
                pState = PM_SEQ_4_SEND_WAIT
                nextSeqReq = 0
                nextPlaySeqReqPub.publish(1)
            elif(pState == PM_SEQ_4_SEND_WAIT):
                if(nextSeqReq == 1):
                    pState = PM_DONE
            elif(pState == PM_DONE):    
                state = COMMAND_MODE
                cState = CM_RESET
                pState = PM_RESET
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