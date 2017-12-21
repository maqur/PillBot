# Navigation

## Dependencies

- RosAria
- move_base `sudo apt-get install ros-kinetic-move-base`
- RPLidar `sudo apt-get install ros-kinetic-rplidar-ros`
- map_server `sudo apt-get install ros-kinetic-map-server`

## Setup
This package assumes that the robot (PeopleBot) is connected at port `/dev/pillbot` and the laser scanner at `/dev/rplidar`. These can be changed directly in the existing launch files.

To use the existing port names add [this](../../ros-independent/99-usb-serial.rules) file in the directory '/etc/udev/rules.d'. The IDs set in the file are for the devices used in the project. For other devices change them as necessary. Check [this](http://hintshop.ludvig.co.nz/show/persistent-names-usb-serial-devices/) for details. 

Change the permissions of the ports used by `sudo chmod 666 -R [PORT]`.

## Running
- Launch configuraton `roslaunch pillbot_nav pillbot_configuration.launch`
- Launch navigation stack `roslaunch pillbot_nav move_base.launch`