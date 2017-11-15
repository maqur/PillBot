#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
from weather import Weather
import math

def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")

def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio, key="AIzaSyDXksdLvMsZvWuAl02ueGeL3_PtEbyN41c")
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
    speak(ctime())

def faranheit_to_celsius(faranheit):
    return ((faranheit - 32)*(5/9))

def london_weather():
    weather = Weather()

    lookup = weather.lookup(44418)
    condition = lookup.condition()
    celsius = math.ceil(faranheit_to_celsius(float(condition.temp()))*10)/10 #round to nearest 0.1 degrees
    speak("It's " + condition.text() + " today with a temperature of " + str(celsius) + " degrees Celsius")

#Think of this like Alexa skills, if the user says something, what should the answer be?
def jarvis(data):

    terminology = data.split(" ") #transform the string to a list

    # if the user says hello
    if find_some_term(terminology,"hi") or find_some_term(terminology,"hello"):
        speak("Hello")

    if "are you my robot" in data:
        speak("yes I am")

    # tell them the time
    if find_some_term(terminology,"time"):
        tell_the_time()

    # find the weather
    if find_some_term(terminology,"weather"):
        london_weather()

    if "what medicine do you have for me" in data:
        speak("I have panadol ibuprofen and xantax")

    if "where is" in data:
        data = data.split(" ")
        location = data[2]
        speak("Hold on PillBot user, I will show you where " + location + " is.")
        os.system("chromium-browser https://www.google.nl/maps/place/" + location + "/&amp;")

# initialization
time.sleep(2)
speak("Hi PillBot user, what can I do for you?")
while 1:
    data = recordAudio()
    jarvis(data)
