# Ros-Independent

This folder primarily contains all the developmental material made by Team PillBot that was not yet imported to ROS. For run instructions on the code see the section below:

## Speech

In order to use the speech folder for performing speech recognition, there are numerous dependencies that need to be installed. This guide will cover the MAC OS X dependencies but the installation should be similar for other platforms.

### Dependencies

Before you begin using the software make sure you have installed Python 3 (It doesn't work with Python 2.x).

The list of dependencies includes:

- pip
- pyAudio
- Speech Recognition Library for python
- gTTS
- mpg321 for MAC OS X

#### pip

Since python comes with OS X pip should be already installed, but on the off chance your python version turns up errors then use homebrew. The simple command would then be `$: brew install python` on terminal.

#### pyAudio

`pip install pyaudio`

#### Speech Recognition Library for python

This is simple after you have pip. The command is `pip install SpeechRecognition` as spotted on [this website](https://pythonprogramminglanguage.com/speech-recognition/)

#### gTTS

`sudo pip install gTTS`

#### mpg321 for MAC OS X

`brew install mpg321`

That should cover your dependencies. If there are any other dependencies post an issue. 

### Usage

Once you have all the dependencies installed navigate to the folder that contains speech. On terminal it should be `cd YOUR_FILE_PATH/speech/` where YOUR_FILE_PATH is the directory you downloaded the speech folder to.

Once you have this working, type the following in terminal:

`$:python3 jarvis.py`

It should come up with a prompt that says "Hi PillBot User! How are you?"

Currently the database that includes all possible prompt responses is limited so the support will only work for prompts like:

1. how are you
2. are you my robot
3. what time is it
4. what medicine do you have for me
5. where is rome

We expect to expand this database for the application! 
