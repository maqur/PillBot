#!/usr/bin/env python

import cv2
import numpy as np
import os
import json
import rospy
from cv_bridge import CvBridge,CvBridgeError
import std_msgs
import sensor_msgs



def detector():

    path='dataSet'
    path_name='names'


    faceDetect=cv2.CascadeClassifier('/home/mikheil/catkin_ws/src/face_det/scripts/haarcascade_frontalface_default.xml')
    
    with open("/home/mikheil/catkin_ws/src/face_det/scripts/names/names.json", 'r') as f:
	    names_dict = json.load(f)
	    
	    


    cam=cv2.VideoCapture(0)

    rec=cv2.face.createLBPHFaceRecognizer()
    rec.load(os.path.abspath("/home/mikheil/catkin_ws/src/face_det/scripts/recognizer/trainingData.yml"))
    id_var=0
    font=cv2.FONT_HERSHEY_COMPLEX_SMALL

    bg=CvBridge()
    pub=rospy.Publisher('face_id',std_msgs.msg.String,queue_size=10)
    pub_2=rospy.Publisher('face_stream',sensor_msgs.msg.Image, queue_size=10)
    
    
    
    rospy.init_node('detector',anonymous=True)


    rate=rospy.Rate(10)



    while(True):
        ret,img=cam.read()
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(w+w,y+h),(0,255,0),2)
            id_var,cong=rec.predict(gray[y:y+h,x:x+w])
            cv2.putText(img,str(names_dict[str(id_var)]),(x,y+h),font,2,(0,0,255),6)
        pub.publish(str(names_dict[str(id_var)]))
        pub_2.publish(bg.cv2_to_imgmsg(img))
        rate.sleep()
		#print(str(names_dict[str(id_var)])+" detected ")
        cv2.imshow("Face",img)
        if(cv2.waitKey(1)==ord('q')):
			break
    cam.release()
    cv2.destroyAllWindows()
	
if __name__=='__main__':
	try:
		detector()
	except rospy.ROSInterruptException:
		pass

		
