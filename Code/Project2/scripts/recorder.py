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

import pyaudio
import wave
from ctypes import *
import sys

#keeps track of the recordings
recordCount = 0

#handshaking signal which will indicate about recording signal
finishRecordPub = rospy.Publisher('RecFinish', Int32, queue_size = 1)
recFilePub = rospy.Publisher('RecFilePath', String, queue_size = 1)


# some values for the recorder
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5

# pyaudio objects
p = None
stream = None
frames = []
rec_data = None

# this part rids of unnessary recorder error messages
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
	return
	
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)

def record(fileName, seconds):
    global rec_data
    global frames
    global p
    global stream
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, input_device_index=None, rate=RATE, input=True, frames_per_buffer=CHUNK)	

    for i in range(0, int(RATE / CHUNK * seconds)):
        rec_data = stream.read(CHUNK)
        frames.append(rec_data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    asound.snd_lib_error_set_handler(None)
    wf = wave.open(fileName, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    rec_data = None
    frames = []
    
'''
def record(fileName, seconds):
    #command to do recording
    bashCommand = "arecord -D plughw:1,0 -d " + str(seconds) + " " + fileName
    os.system(bashCommand)
'''

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