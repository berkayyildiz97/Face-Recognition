import cv2
import dlib
import numpy as np
import os
import sys
import Database_helper
import face_gui
from torch_neural_net import TorchNeuralNet
import FaceAligner

net = TorchNeuralNet()	

def align(fileName):
	shape_predictor = "shape_predictor_68_face_landmarks.dat"
	image = cv2.imread(fileName)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		
	detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	#default scale factor = 1.3,1.04 de iyi
	
	rects = detector.detectMultiScale(gray, scaleFactor=1.2,minNeighbors=10, minSize=(75, 75))
	i=0.01
	while True:
		if len (rects)!=0:
			break
		if 1.2-i <= 1:
			print("Couldn't find a face")
			break
		else:
			rects = detector.detectMultiScale(gray, scaleFactor=1.2-i,
			minNeighbors=10, minSize=(75, 75))
		i=i+0.01;
	#rects = detector.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=10, minSize=(75, 75))
	predictor = dlib.shape_predictor(shape_predictor)
	fa = FaceAligner.FaceAligner(predictor, desiredFaceWidth=96)

	faceAligned = None

	for (i, rect) in enumerate(rects):
		x = rect[0]
		y = rect[1]
		w = rect[2]
		h = rect[3]

		rect = dlib.rectangle(x, y, x + w, y + h)
		#shape = predictor(gray, rect)
		#shape = shape_to_np(shape)
	    	# Face Normalization   
		faceAligned = fa.align(image, gray, rect)
		cv2.imshow("Aligned", faceAligned)
		cv2.waitKey(0)
	return faceAligned	

Database_helper.setDatabase('Lfw_Database2.db')
for root, directories, filenames in os.walk('/home/berkay/FaceRecog2/lfw'):
	for filename in filenames:
		faceName = filename.split('.')[0]
		filename = os.path.join(root,filename)
		faceAligned_RGB = align(filename)
		if(faceAligned_RGB is None):
			continue
		embeddings = net.forward(faceAligned_RGB)
		if Database_helper.isFound(embeddings) == False:
			Database_helper.record(embeddings,faceName)
		else:
			print "Already registered"




