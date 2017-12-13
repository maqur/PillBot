import cv2
import numpy as np
import os
import json

path='dataSet'
path_name='names'


faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

with open(os.path.abspath(os.path.join(path_name,'names.json')), 'r') as f:
    names_dict = json.load(f)
    
    


cam=cv2.VideoCapture(0)

rec=cv2.face.createLBPHFaceRecognizer()
rec.load(os.path.abspath("recognizer/trainingData.yml"))
id_var=0
font=cv2.FONT_HERSHEY_COMPLEX_SMALL
while(True):
	ret,img=cam.read()
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	faces=faceDetect.detectMultiScale(gray,1.3,5)
	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(w+w,y+h),(0,255,0),2)
		id_var,cong=rec.predict(gray[y:y+h,x:x+w])
		cv2.putText(img,str(names_dict[str(id_var)]),(x,y+h),font,2,(0,0,255),6)
	cv2.imshow("Face",img)
	if(cv2.waitKey(1)==ord('q')):
		break
cam.release()
cv2.destroyAllWindows()
	
		
