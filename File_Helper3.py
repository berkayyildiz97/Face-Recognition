import cv2
import dlib
import numpy as np
import os
import sys
import Database_helper
import face_gui
from torch_neural_net import TorchNeuralNet
import FaceAligner
import face_gui
from Tkinter import *

root = Tk()

net = TorchNeuralNet()
Database_helper.setDatabase('Lfw_Database4.db')
for root, directories, filenames in os.walk('/home/berkay/FaceRecog2/lfw'):
	for filename in filenames:
		print "filename:",filename
		faceName = filename.split('.')[0]
		filename = os.path.join(root,filename)
		faceAligned_RGB = None
		(image_return,faceAligned_return,image,faceAligned_RGB) = face_gui.startDetection(filename)
		if(faceAligned_RGB is None):
			continue
		embeddings = net.forward(faceAligned_RGB)
		Database_helper.record(embeddings,faceName)

'''
net = TorchNeuralNet()
Database_helper.setDatabase('database.db')
filename= '/home/berkay/FaceRecog2/lfw/Steve_Spurrier/Steve_Spurrier_0002.jpg'
faceName = filename.split('.')[0]
faceAligned_RGB = None
(image_return,faceAligned_return,image,faceAligned_RGB) = face_gui.startDetection(filename)
cv2.imshow("Aligned", faceAligned_RGB)
cv2.waitKey(0)
embeddings = net.forward(faceAligned_RGB)
Database_helper.record(embeddings,faceName)
'''




