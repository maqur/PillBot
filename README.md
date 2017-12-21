# PillBot

## Setup

- Clone repository `git clone --recursive https://github.com/maqur/PillBot.git`
- Complile `catkin_make`

## Running

- Soure the PillBot workspace `source devel/setup.bash`
- Launch all the nodes `roslaunch brain pillbot.launch` 
- Give the name and location of patient `rosrun navigation_goals simple_navigation_goals`
- Where necessary go to https://humancrob.herokuapp.com to add a patient to the database with prescription

## Dependencies

- All the files must be launched from the cloned directory for correct paths
- [ARIA](http://robots.mobilerobots.com/wiki/Aria)
- [Navigation](src/pillbot_nav/README.md) 
- [Speech](src/speech/README.md) 
- [Facial Recognition](src/face_det/README.md)
- [Mood Detection](src/facemoji/README.md)

