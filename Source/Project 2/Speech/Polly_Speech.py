import boto3
from pygame import mixer
import os

polly = boto3.client('polly')
spoken_text = polly.synthesize_speech(Text='Hi, I am newtonBOT.', OutputFormat='mp3', VoiceId = 'Emma')

#write binary to file
with open('textToSpeech.mp3', 'wb') as f:
    f.write(spoken_text['AudioStream'].read())
    f.close()

#play in script the sound track
mixer.init()
mixer.music.load('output.mp3')
mixer.music.play()

while mixer.music.get_busy() == True:
    pass
#quit mixer
mixer.quit()
#remove file 
#os.remove('textToSpeech.mp3')
