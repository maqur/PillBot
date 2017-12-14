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
    print("running the listener ")
    rospy.loginfo(rospy.get_caller_id() +"I heard %s",data.data)
    detect(data.data)

def detect(target):
    path='dataSet'
    path_name='names'
      
    #target=raw_input("Please enter name of the target : ")
    print("running detector")
    faceDetect=cv2.CascadeClassifier('/home/human/PillBot/src/face_det/scripts/haarcascade_frontalface_default.xml')
    
    with open("/home/human/PillBot/src/face_det/scripts/names/names.json", 'r') as f:
	    names_dict = json.load(f)
	    
	    


    cam=cv2.VideoCapture(1)

    rec=cv2.face.createLBPHFaceRecognizer()
    rec.load(os.path.abspath("/home/human/PillBot/src/face_det/scripts/recognizer/trainingData.yml"))
    id_var=0
    font=cv2.FONT_HERSHEY_COMPLEX_SMALL

    bg=CvBridge()
    pub=rospy.Publisher('face_id',std_msgs.msg.String,queue_size=10)
    pub_2=rospy.Publisher('face_stream',sensor_msgs.msg.Image, queue_size=10)
     
    rate=rospy.Rate(10)

    while(True):
        ret,img=cam.read()
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(w+w,y+h),(0,255,0),2)
            id_var,cong=rec.predict(gray[y:y+h,x:x+w])
            cv2.putText(img,str(names_dict[str(id_var)]),(x,y+h),font,2,(0,0,255),6)

        if str(names_dict[str(id_var)]) == target:
            pub.publish(str(names_dict[str(id_var)]))
	    old_image = bg.cv2_to_imgmsg(img, encoding="passthrough")
            pub_2.publish(old_image)
	    new_image = bg.imgmsg_to_cv2(old_image, desired_encoding="passthrough")
            id_var=0
        else:
            pub.publish("Target not detected ")
        rate.sleep()
		#print(str(names_dict[str(id_var)])+" detected ")
        cv2.imshow("Face",img)
        if(cv2.waitKey(1)==ord('q')):
			break
    cam.release()
    cv2.destroyAllWindows()
    

def detector():

    path='dataSet'
    path_name='names'
    print("loading main mehtod ")
    
    rospy.init_node('detector',anonymous=True)

    rospy.Subscriber("name", std_msgs.msg.String, callback)
   
    rospy.spin()

	
if __name__=='__main__':
	try:
		detector()
	except rospy.ROSInterruptException:
		pass

		
