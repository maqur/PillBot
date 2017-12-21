# PillBot

## Setup

- Clone repository `git clone --recursive https://github.com/maqur/PillBot.git`
- Complile `catkin_make`

## Running

- Soure the PillBot workspace `source devel/setup.bash`
- Launch all the nodes `roslaunch brain pillbot.launch` (launch from the PillBot directory)
- Give the name and location of patient `rosrun navigation_goals simple_navigation_goals`

## Dependencies

- [ARIA](http://robots.mobilerobots.com/wiki/Aria)
- [Navigation](src/pillbot_nav/README.md) dependencies
- [Speech](src/speech/README.md) dependencies
- [Facial Recognition](src/face_det/README.md)
- [Mood Detection](src/facemoji/README.md)

