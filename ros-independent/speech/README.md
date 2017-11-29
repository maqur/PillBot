# Ros-Independent

This folder primarily contains all the developmental material made by Team PillBot that was not yet imported to ROS. For run instructions on the code see the section below:

## Speech

In order to use the speech folder for performing speech recognition, there are numerous dependencies that need to be installed. This guide will cover the MAC OS X dependencies but the installation should be similar for other platforms. (Update: the same methodology works for linux Ubuntu)

### Dependencies

Before you begin using the software make sure you have installed Python 3 (It doesn't work with Python 2.x).

The list of dependencies includes:

- pip
- pyAudio
- Speech Recognition Library for python
- gTTS
- mpg321
- RASA NLU for the Chatbot AI

#### pip

Since python comes with OS X pip should be already installed, but on the off chance your python version turns up errors then use homebrew. The simple command would then be `$: brew install python` on terminal.

#### pyAudio

`pip3 install pyaudio`

for Linux:

- `sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0`
- `sudo apt-get install ffmpeg libav-tools`
- `sudo pip3 install pyaudio`

#### Speech Recognition Library for python

This is simple after you have pip. The command is `pip install SpeechRecognition` as spotted on [this website](https://pythonprogramminglanguage.com/speech-recognition/)

#### gTTS

`sudo pip3 install gTTS`

#### mpg321 

for MAC OS X:

- `brew install mpg321`

for Ubuntu: 

- `sudo apt-get update`
- `sudo apt-get install mpg321`

#### RASA NLU

For rasa nlu there are two counter-intuitive things to do and a couple of extra things to add:

- First pip install rasa: `$: pip3 install rasa_nlu`
- Then clone RASA NLU into the speech folder directory so you should have `YOUR_PATH/speech/rasa_nlu` (cloning can be done on the website: https://github.com/RasaHQ/rasa_nlu) (this is due to the way the code calls the training model) 
- These are the extraneous dependencies to install also detailed in the RASA documentation: `$: sudo pip3 install -U spacy` and then `$: python3 -m spacy download -en` followed by the final dependency `$: pip3 install -U scikit-learn scipy sklearn-crfsuite`

That should cover your dependencies. If there are any other dependencies post an issue. 

### Usage

Once you have all the dependencies installed navigate to the folder that contains speech. On terminal it should be `cd YOUR_FILE_PATH/speech/` where YOUR_FILE_PATH is the directory you downloaded the speech folder to.

Once you have this working, type the following in terminal:

`$:python3 jarvis.py`

It should come up with a prompt that says "Hello PillBot user?" followed by "Please wait! Calibrating microphone." then a 2 second pause to adjust the microphone to ambient noise followed by "Calibration complete, ask me what you want" 

Currently the database that includes all possible prompt responses is limited so the support will only work for prompts like:

1. hello
2. how are you
3. what time is it
4. what's the weather like

We expect to expand this database for the application! 
