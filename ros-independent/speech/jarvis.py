#!/usr/bin/env python3
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


#The dictionary of all responses to intents
PillBot_response = {
    'greet' : ["Hello","Howdy","Hi Afraz"],
    'greet_response' : ["I'm good","It's all great","Just coughing up pills"],
    'affirm' : ["ok","great","ok, perfect","splendid"],
    'goodbye' : ["Goodbye","See you later","Sayonara","Till next time then"]
}

def speak(audioString):
    tts = gTTS(text=audioString, lang='en-us')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")

def recordAudio(calibrated):
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if not calibrated:
            speak("Please wait! Calibrating microphone")
            print("Please wait! Calibrating microphone")
            #Listen for 5 seconds to adjust for ambient noise
            r.adjust_for_ambient_noise(source, duration = 3)
            speak("Calibration complete, ask me what you want")
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
    print(intent)
    # if the user says hello
    if intent == 'greet':
        choose_idx = randint(0,len(PillBot_response['greet']) - 1)
        speak(PillBot_response['greet'][choose_idx])
    if intent == 'greet_response':
        choose_idx = randint(0,len(PillBot_response['greet_response']) - 1)
        speak(PillBot_response['greet_response'][choose_idx])
    if intent == 'affirm':
        choose_idx = randint(0,len(PillBot_response['affirm']) - 1)
        speak(PillBot_response['affirm'][choose_idx])
    if intent == 'goodbye':
        choose_idx = randint(0,len(PillBot_response['goodbye']) - 1)
        speak(PillBot_response['goodbye'][choose_idx])        
    # tell them the time
    if intent == 'time':
        tell_the_time()

    if "how old are you" in data:
        speak("I was born yesterday")
    # find the weather
    if intent == 'weather':
        london_weather()

    if "tell me a joke" in data or "say something funny" in data:
        speak("Why was 6 afraid of 7?")
        time.sleep(1)
        speak("Because 7 8 9")

    if "what medicine do you have for me" in data:
        speak("I have panadol ibuprofen and xantax")


def main():
    #Perform machine learning model train first:
    #the load data command looks for a JSON file of your training data in the directory you have it stored, just input file-name if in same directory.
    training_data = load_data('rasa_nlu/data/examples/rasa/demo-rasa.json')
    #Wherever you have git cloned rasa_nlu it will look for Spacy's configuration of the JSON file
    trainer = Trainer(RasaNLUConfig("rasa_nlu/sample_configs/config_spacy.json"))
    #this just trains based on the training data
    trainer.train(training_data)

    model_directory = trainer.persist('./projects/default/')  # Returns the directory the model is stored in

    # where `model_directory points to the folder the model is persisted in
    interpreter = Interpreter.load(model_directory, RasaNLUConfig("rasa_nlu/sample_configs/config_spacy.json"))

    speak("Hello PillBot User!")
    calibrated = False
    while 1:
        data = recordAudio(calibrated)
        jarvis(data,interpreter)
        calibrated = True
# initialization
time.sleep(2)
if __name__ == "__main__":
    main()
