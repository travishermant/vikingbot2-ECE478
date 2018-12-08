#!/usr/bin/env python

import dialogflow_v2 as dialogflow
import os

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
from time import sleep

#export the file json file for credentials
#FIXME get the file location from constants
#os.system('export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/catkin_ws/src/project2/jsonfile/robotics-test-ca3667416a35.json"')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/catkin_ws/src/project2/jsonfile/robotics-test-ca3667416a35.json"

speechRecString = rospy.Publisher('SpeechRecString', String, queue_size = 1)

session_client = None

#function where all the magic happens
def detect_intent_audio(project_id, session_id, audio_file_path,
                        language_code):
    global session_client
    session_client = dialogflow.SessionsClient()

    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 16000

    session = session_client.session_path(project_id, session_id)

    with open(audio_file_path, 'rb') as audio_file:
        input_audio = audio_file.read()

    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)
    query_input = dialogflow.types.QueryInput(audio_config=audio_config)

    response = session_client.detect_intent(
        session=session, query_input=query_input,
        input_audio=input_audio)

    return response.query_result.fulfillment_text

def do_recognise(data):
    '''
    try:
        result = detect_intent_audio("robotics-test-478f7", "1-1-1-1-1", data.data, 'en-US')
        print(result)
        speechRecString.publish(result)
    except:
        print("something is wrong")
        speechRecString.publish('')
    '''
    speechRecString.publish('theater')

def speech_recogniser_node():
    rospy.init_node('speech_recogniser_node')
    rospy.Subscriber('RecogniseCommand', String, do_recognise)
    rospy.spin()

if __name__ == '__main__':
    print("ready for speech recognistion")
    try:
        speech_recogniser_node()
    except rospy.ROSInterruptException():
        pass