import cv2
import numpy as np
import json
import os


faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cam=cv2.VideoCapture(1)

path="dataSet"
path_name="names"

with open(os.path.abspath(os.path.join(path_name,'names.json')), 'r') as f:
    names_dict = json.load(f)

name=input('enter user id  ')

while(str(name) in names_dict):
    print("This ID already exists")
    name=input('enter user id  ')


sampleNum=0

string=raw_input('Please enter the corresponding username ')

names_dict[str(name)]=string

with open(os.path.abspath(os.path.join(path_name,'names.json')), 'w') as f:
    json.dump(names_dict, f)

while(True):
	ret,img=cam.read()
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	faces=faceDetect.detectMultiScale(gray,1.3,5)
	for (x,y,w,h) in faces:
		sampleNum=sampleNum+1
		cv2.imwrite("dataSet/User."+str(name)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
		cv2.rectangle(img,(x,y),(w+w,y+h),(0,255,0),2)
		cv2.waitKey(1000);
	cv2.imshow("Face",img)
	cv2.waitKey(1)
	if(sampleNum>20):
		break

cam.release()
cv2.destroyAllWindows()
	
