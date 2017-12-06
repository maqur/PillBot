import os
import cv2
import json


import numpy as np
from PIL import Image



recognizer=cv2.face.createLBPHFaceRecognizer()
#recognizer=cv2.
path='dataSet'


def getImageID(path):
	imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
	faces=[]
	IDs=[]
	for imagePath in imagePaths:
		faceImg=Image.open(imagePath).convert('L')
		faceNp=np.array(faceImg,dtype=np.uint8)
		ID=int(os.path.split(imagePath)[-1].split('.')[1])
		sampleNum=int(os.path.split(imagePath)[-1].split('.')[2])
		faces.append(faceNp)
		IDs.append(ID)
		cv2.imshow("training",faceNp)
		cv2.imwrite("dataSet/User."+str(ID)+"."+str(sampleNum)+".jpg",faceNp)
		cv2.waitKey(10)
	return IDs,faces

IDs,faces=getImageID(path)

recognizer.train(faces,np.array(IDs))
recognizer.save('recognizer/trainingData.yml')
cv2.destroyAllWindows()
#	print(imagePaths)
	
#getImageID(path)
