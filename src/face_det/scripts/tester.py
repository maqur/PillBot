#!/usr/bin/env python


import cv2
import numpy as np
import os
import json



cam=cv2.VideoCapture(0)


while(True):
	ret,img=cam.read()
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	cv2.imshow("Face",gray)
	if(cv2.waitKey(1)==ord('q')):
		break
    
    
    
cam.release()
cv2.destroyAllWindows()
	