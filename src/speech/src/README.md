
# Speech

In order to use the speech folder for performing speech recognition, there are numerous dependencies that need to be installed. This guide will cover the MAC OS X dependencies but the installation should be similar for other platforms. (Update: the same methodology works for linux Ubuntu)

Note: The dependencies do not cover the ones required for ROS. The entire framework for the PillBot application utilises ros-kinetic, the guide for installation can be found [here](http://wiki.ros.org/kinetic/Installation/Ubuntu). The CMakes and package.xml assume an already installed rospy or std\_msgs(). 

## Dependencies

Before you begin using the software make sure you have installed Python 2 (It doesn't work with Python 3.x).

The list of dependencies includes:

- pip
- pyAudio
- Speech Recognition Library for python
- Google API Library for python
- Yahoo Weather API
- gTTS
- mpg321
- RASA NLU for the Chatbot AI

### pip

Since python comes with OS X pip should be already installed, but on the off chance your python version turns up errors then use homebrew. The simple command would then be `$: brew install python` on terminal.

### pyAudio

`sudo pip install pyaudio`

for Linux:

- `sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0`
- `sudo apt-get install ffmpeg libav-tools`
- `sudo pip install pyaudio`

### Speech Recognition Library for python

This is simple after you have pip. The command is `sudo pip install SpeechRecognition` as spotted on [this website](https://pythonprogramminglanguage.com/speech-recognition/)

### Google API Library for python

`sudo pip install google-api-python-client`

### Yahoo Weather API

`sudo pip install weather-api`

### gTTS

`sudo pip install gTTS`

### mpg321 

for MAC OS X:

- `brew install mpg321`

for Ubuntu: 

- `sudo apt-get update`
- `sudo apt-get install mpg321`

### RASA NLU

For rasa nlu there are two counter-intuitive things to do and a couple of extra things to add:

- First pip install rasa: `$ sudo pip install rasa_nlu`
- Then clone RASA NLU into the speech folder directory so you should have `YOUR_PATH/speech/rasa_nlu` (cloning can be done on the website: https://github.com/RasaHQ/rasa_nlu) (this is due to the way the code calls the training model) 
- These are the extraneous dependencies to install also detailed in the RASA documentation: `$ sudo pip install -U spacy` and then `$: python -m spacy download en` followed by the final dependency `$ sudo pip install -U scikit-learn scipy sklearn-crfsuite`

That should cover your dependencies. If there are any other dependencies post an issue. 

## Usage

First you must launch a roscore which can be done in terminal by:

`$ roscore `

Then type the following in a new terminal window:

`$ rosrun speech jarvis.py`

Please note that the program must be made executable in ROS by doing chmod +x jarvis.py (given that you are in the directory ~/PillBot/src/speech/src/). A `catkin_make` is necessary to compile the program once before you move on towards utilising it in ROS. 

It should come up with a prompt that says "Hello PillBot user?" followed by "Please wait! Calibrating microphone." then a 2 second pause to adjust the microphone to ambient noise followed by "Calibration complete, ask me what you want" 

Currently the database that includes all possible prompt responses is limited so the support will only work for prompts like:

1. hello
2. how are you
3. what time is it
4. what's the weather like

We expect to expand this database for the application! 

## Additional Notes

Here are some common issues with dependencies or usage:

Q) The program seems to utilise python2 but I have python3 installed

A) On any macbook or linux laptop you should have python 2 automatically installed. If you do not have it on Linux then you must do `sudo-apt get install python(version number)` please replace (version number) with a version like 2.7 or leave it blank and it should still install python 2.x

Q) pip consistently installs programs in areas that aren't using the current version of python I have

A) By typing pip, it should revealed where the default directory to pip is for applications to be utilised in python. Most pips tend to point to python2 but on some occassion during configuration on certain laptops the default pip actually points to python3 which is why none of the dependencies would seem to be found or utilised by jarvis. To overcome this try using `pip2` in all the above installation dependencies. 

Q) The program gets stuck on "Say something!"

A) There could be multiple reasons for this. The best troubelshooting one would be through the quality of the current internet connection. Most tests revealed that it requires around 30-35 Mbps. Imperials internet gives no errors or flaws in it. Another reason could be that multiple people are talking at once which limits its usage as it is trying to understand more people (much like how we try to listen to someone in a crowd when everyone is talking). This can be rectified by tuning the Microphone from the GUI in the sound bar in Linux to make the amplification small so ambient noise is eliminated as much as possible. A good indicator is around 30% in most tests. And finally if none of the above work the best reasoning behind it could be the number of processes occurring on a laptop at once. While running the program numerous times I found that even having a browser open can siphon a lot of the processing required by the programming so try to close all windows except for the ones required for the tests.

Q) I have issues with using RASA (like could not load trainer)

A) As RASA is quite complicated with the documentation my best recommendation to avoiding any errors with RASA would be (assuming you installed the dependencies correctly), run a `git clone https://github.com/RasaHQ/rasa_nlu.git` and install it in the same directory as speech, then in the code navigate to the relevant lines in jarvis.py (lines 120, 122 and 126) to change the directory accordingly. Given that this is now using a default training data implementation, please use the training data on my personal GitHub [here](https://github.com/Afrazinator/rasa_nlu/blob/master/data/examples/rasa/demo-rasa.json). You can copy this training data and paste it to the same directory under ~PillBot/src/speech/src/rasa\_nlu/data/examples/rasa/demo-rasa.json and paste it into this json. 

If there are any further issues please send me an email at afrazarif@hotmail.com
