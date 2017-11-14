# Connecting to PeopleBot using ROSARIA

## Packages required
- ROSARIA

## Setup
- Connect the serial port on the robot with computer through USB
- Check the open usb port `ls -l /dev/ | grep ttyUSB`
- Change permissions of the port used for robot (`ttyUSB1` here) `sudo chmod 777 -R /dev/ttyUSB1`
- Start roscore `roscore`
- Run rosaria node `rosrun rosaria RosAria`
- If the robot does not connect specify the port (`ttyUSB1` here) `rosrun rosaria RosAria _port:=/dev/ttyUSB1`
- Check [ROSARIA tutorial](http://wiki.ros.org/ROSARIA/Tutorials/How%20to%20use%20ROSARIA) in case of problems


