#!/usr/bin/env python

import boto3
import rospy

#import actionlib
from std_msgs.msg import String, Bool
from std_msgs.msg import Int32
import time

tTSDone = rospy.Publisher('TTSDone', Int32, queue_size = 1)

polly_client = boto3.Session(aws_access_key_id="AKIAJ5MQYS4JLJFRGS3A",                     
        aws_secret_access_key="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",
        region_name='us-west-2').client('polly')

def speak_callback(data):
    global polly_client
    response = polly_client.synthesize_speech(VoiceId='Brian',
                OutputFormat='mp3', Text = data.data)

    file = open('/home/pi/catkin_ws/src/project2/wav/speech.mp3', 'w')
    file.write(response['AudioStream'].read())
    file.close()
    time.sleep(1)
    tTSDone.publish(1)

def polly_speech_node():
    print("Polly Node Initialised")
    # Initializing the ROS node "polly_speech"    
    rospy.init_node('polly_speech', anonymous=True)
    # Creating Subscriber topics for Listen
    rospy.Subscriber("TTSReq",String,speak_callback)
    rospy.spin()
    
if __name__ == '__main__':
    try:
        polly_speech_node()
    except rospy.ROSInterruptexception:
        pass