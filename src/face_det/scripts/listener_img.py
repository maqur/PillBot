#!/usr/bin/env python
import cv2
import numpy as np
import os
import json
import rospy
from cv_bridge import CvBridge,CvBridgeError
import std_msgs
import sensor_msgs



def callback(data):
    br=CvBridge()
    cv2.imshow("ros feed",br.imgmsg_to_cv2(data))
    rospy.loginfo("SHowing image feed...")
    cv2.waitKey(100)



def listener():
    rospy.init_node ('listener_img', anonymous=True)
    rospy.Subscriber("face_stream", sensor_msgs.msg.Image, callback)
    rospy.spin()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    listener()