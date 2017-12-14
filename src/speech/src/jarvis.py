#!/usr/bin/env python
# Requires PyAudio and PySpeech.

import speech_recognition as sr
from time import ctime
import time
from datetime import datetime
import os
from gtts import gTTS
from weather import Weather
import math
from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer, Metadata, Interpreter
from random import *
import rospy
from std_msgs.msg import String
import http.client
import json


#The dictionary of all responses to intents
PillBot_response = {
    'greet' : ["Hello","Howdy","Hi Afraz"],
    'greet_response' : ["I'm good","It's all great","Just coughing up pills"],
    'affirm' : ["ok","great","ok, perfect","splendid"],
    'goodbye' : ["Goodbye","See you later","Sayonara","Till next time then"]
}

pills_data = []

def speak(audioString):
    tts = gTTS(text=audioString, lang='en-us')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")

def recordAudio(calibrated):
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if not calibrated:
            print("Please wait! Calibrating microphone")
            #Listen for 5 seconds to adjust for ambient noise
            r.adjust_for_ambient_noise(source, duration = 1)

        print("Say something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return data

def find_some_term(terminology,find_me):
    for i in range(0,len(terminology)):
        if(terminology[i] == find_me):
            return True
    return False

def tell_the_time():
    print(time.strftime("%c", time.gmtime()))
    speak(ctime())

def faranheit_to_celsius(faranheit):
    return ((faranheit - 32)*(5/9))

def london_weather():
    weather = Weather()
    lookup = weather.lookup(44418)
    condition = lookup.condition()
    celsius = math.ceil(faranheit_to_celsius(float(condition.temp()))*10)/10 #round to nearest 0.1 degrees
    speak("In London it's " + condition.text() + " today with a temperature of " + str(celsius) + " degrees Celsius")

#Think of this like Alexa skills, if the user says something, what should the answer be?
def jarvis(data,interpreter):

    #The interpreter variable is a dict that can be parsed to release intents
    response = interpreter.parse(data)
    terminology = data.split(" ") #transform the string to a list
    intent = response['intent']['name']
    confidence = response['intent']['confidence']
    print(confidence)
    if confidence > 0.42:
        if intent == 'greet':
            choose_idx = randint(0,len(PillBot_response['greet']) - 1)
            speak(PillBot_response['greet'][choose_idx])
        if intent == 'greet_response':
            choose_idx = randint(0,len(PillBot_response['greet_response']) - 1)
            speak(PillBot_response['greet_response'][choose_idx])
        if intent == 'affirm' and confidence > 0.5:
            choose_idx = randint(0,len(PillBot_response['affirm']) - 1)
            speak(PillBot_response['affirm'][choose_idx])
        if intent == 'goodbye':
            choose_idx = randint(0,len(PillBot_response['goodbye']) - 1)
            speak(PillBot_response['goodbye'][choose_idx])
        # tell them the time
        if intent == 'time':
            tell_the_time()
        if intent == 'weather':
            london_weather()
    elif confidence < 0.42 and confidence > 0.01 :
        speak("I did not understand what you said, please repeat that")

    if "how old are you" in data:
        speak("I was born yesterday")

    if "tell me a joke" in data or "say something funny" in data:
        speak("Why was 6 afraid of 7?")
        time.sleep(1)
        speak("Because 7 8 9")

    end_method(intent)

def end_method(intent):
    return intent

def callback2(data):
    talking_to_PillBot_user_first_time(data.data)

def talking_to_PillBot_user_first_time(mood_data):
    return mood_data


def meeting_PillBot_user(name_of_user,pills_data):
    speak("Hello " + name_of_user + ". I will be giving you your pills today!")
    calibrated = False
    pill1 =  pills_data[0]
    pill2 =  pills_data[1]
    rospy.Subscriber("mood",String,callback2)
    mood_obj = rospy.wait_for_message("mood", String, timeout=20)
    mood = mood_obj.data
    #mood = "happy"
    time.sleep(2)
    speak("You look " + mood + " today!")
    print("You look " + mood + " today!")
    time.sleep(1)
    speak("You have " + pill1 + " paracetamol and " + pill2 + " panadol")
    time.sleep(1)
    speak("Can you confirm that these are your pills? Say yes if they are or no if they are not")
    expected_response = False
    data = recordAudio(calibrated)
    calibrated = True
    while(not expected_response):
        if(data == "yes"):
            speak("Great,dispensing your pills now")
            time.sleep(1)
            expected_response = True
            pub2 = rospy.Publisher('dispense_pills_now',String,queue_size=10)
            rospy.loginfo("1")
            time.sleep(2)
            pub2.publish("1")
            time.sleep(40)
        elif(data == "no"):
            expected_response = True
            speak("Sorry, calling PillBot engineers now")
        else:
            speak("Could you repeat that?")
            calibrated = False
            data = recordAudio(calibrated)
            calibrated = True
            continue




def callback(name_data):
        #Perform machine learning model train first:
        #the load data command looks for a JSON file of your training data in the directory you have it stored, just input file-name if in same directory.

        pub3 = rospy.Publisher('end',String,queue_size=10)

        training_data = load_data('/home/human/PillBot/ros-independent/speech/rasa_nlu/data/examples/rasa/demo-rasa.json')
        #Wherever you have git cloned rasa_nlu it will look for Spacy's configuration of the JSON file
        trainer = Trainer(RasaNLUConfig("/home/human/PillBot/ros-independent/speech/rasa_nlu/sample_configs/config_spacy.json"))
        #this just trains based on the training data
        trainer.train(training_data)

        model_directory = trainer.persist('./projects/default/')  # Returns the directory the model is stored in

        # where `model_directory points to the folder the model is persisted in
        interpreter = Interpreter.load(model_directory, RasaNLUConfig("/home/human/PillBot/ros-independent/speech/rasa_nlu/sample_configs/config_spacy.json"))
        pills_data = get_pill_data(name_data.data)
        rate = rospy.Rate(10)
        pub = rospy.Publisher('what_user_said', String, queue_size=10)
        meeting_PillBot_user(name_data.data,pills_data)

        time.sleep(1)
        calibrated = False


        speak("Goodbye" + name_data.data)
        pub3.publish("end")
        expected_response = False
        wants_to_converse = False
        data = recordAudio(calibrated)
        calibrated = True
        time.sleep(1)
        while(not expected_response):
            if(data == "yes"):
                expected_response = True
                wants_to_converse = True
            elif(data == "no"):
                expected_response = True
                wants_to_converse = False
            else:
                time.sleep(3)
                #speak("Could you repeat that?")
                data = recordAudio(calibrated)
                continue
        if(wants_to_converse):
            while not rospy.is_shutdown():
                data = recordAudio(calibrated)
                rospy.loginfo(data)
                pub.publish(data)
                rate.sleep()
                jarvis(data,interpreter)
                if end_method == 'goodbye':
                    break
        pub3.publish("end")

def get_pill_data(name):
    conn = http.client.HTTPSConnection("box-6748659.us-east-1.bonsaisearch.net")

    headers = {
        'authorization': "Basic NTh5NWNrNmU6djdvY3c3NWY3MjlxYXp3NQ==",
        'cache-control': "no-cache",
        }
    url =  "/try/try/" + name
    conn.request("GET", url, headers=headers)

    res = conn.getresponse()
    data = json.loads(res.read())

    paracetamol = data["_source"]["paracetamol"]
    panadol = data["_source"]["panadol"]

    return [paracetamol, panadol]

def main():

    rospy.init_node('speechrec', anonymous=True)

    rospy.Subscriber("name",String,callback)
    rospy.spin()

# initialization
time.sleep(2)

if __name__ == "__main__":
    main()
