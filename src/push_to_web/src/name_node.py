#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String


def talker():
    name_of_person = raw_input("Enter the name ")
    pub = rospy.Publisher('name', String, queue_size=10)
    rospy.init_node('name', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    rospy.loginfo(name_of_person.lower())
    pub.publish(str(name_of_person.lower()))
    rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
