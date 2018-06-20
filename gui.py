from Tkinter import *
import tkMessageBox
import tkFileDialog
from PIL import Image
from PIL import ImageTk
import argparse
import cv2
import dlib
import numpy as np
import face_gui
import os
import os.path
import sys
import sqlite3
	
from torch_neural_net import TorchNeuralNet
import Database_helper
window = Tk()
frame = Frame(window)
frame.pack()

bottomFrame =Frame(window)
bottomFrame.pack( side = BOTTOM )

topFrame = Frame(window)
topFrame.pack( side = BOTTOM )
global panelA
global panelB
global panelMiddle
panelA=None
panelB=None
panelMiddle=None
original = None
aligned = None
detectedImage = None
faceAligned_RGB = None
fileName=None
faceName= None
face_name=None
embeddings= None
net=None
thresholdValue=0.0

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--database",
			default="database.db",
			help="path to database")
ap.add_argument("-t", "--threshold",
			default="compute",
			help="threshold value")
args = vars(ap.parse_args())
Database_helper.setDatabase(args["database"])

print "arg1:", args["database"]
print "arg2:", args["threshold"]

if args["threshold"] == "compute":
	thresholdValue = Database_helper.findInitialThresholdValue()
else:
	thresholdValue = float(args["threshold"])
print "thresholdValue",thresholdValue

def clickedImage():
	global panelA,panelB,panelMiddle
	global original,aligned,detectedImage,faceAligned_RGB
	global fileName

	#tkMessageBox.showinfo('Message title', 'Message content')
	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	fileName = tkFileDialog.askopenfilename( title = "Select image") 
	# show an "Open" dialog box and return the path to the selected file
	
	(original,aligned,detectedImage,faceAligned_RGB) = face_gui.startDetection(fileName)
	print("File name: ",fileName)

	# if the panels are None, initialize them
	if panelA is None or panelB is None:	
		
		#the first panel will store our original image
		panelA = Label(topFrame,image=original )
		panelA.image = original
		#panelA.pack(side="left", padx=10, pady=10)
		#panelA.pack(side="left") 
		panelA.grid(row=0,column=1)
		
		# while the second panel will store the edge map
		panelB = Label(topFrame,image=aligned)
		panelB.image = aligned
		#panelB.pack(side="right", padx=10, pady=10)
 		#panelB.pack(side="right") 
		panelB.grid(row=1,column=0)

		panelMiddle = Label(topFrame,image=detectedImage )
		panelMiddle.image = detectedImage
		#panelMiddle.pack(side="left", padx=100, pady=10)
 		#panelMiddle.pack(side="left")
		panelMiddle.grid(row=1,column=2) 		
	# otherwise, update the image panels
	else:
		# update the pannels
		panelA.configure(image=original)
		panelB.configure(image=aligned)
		panelMiddle.configure(image=detectedImage)
		
		panelA.image = original
		panelB.image = aligned
		panelMiddle.image = detectedImage

def saveAlignedImage(imgObject):
	global original,aligned,detectedImage,faceAligned_RGB
	global fileName, face_name, faceName
	mylist = fileName.split('/')
	print(mylist)
	index = len(mylist)
	face_file_name = mylist[index-2]
	face_name = mylist[index-1]
	faceName = face_name.split('.')[0]
	#print("face name: ",face_name)
	#print("face_file_name:" ,face_file_name)
	fileName = fileName.replace("images2","aligned-images")
	os.chdir("aligned-images")
	isFound = os.access(face_file_name, os.F_OK)
	if(isFound == False):	
		os.mkdir(face_file_name)
	os.chdir(face_file_name)
	cv2.imwrite(face_name, imgObject)

	os.chdir("/home/berkay/FaceRecog2")



def clickedRegister():
	global panelA,panelB,panelMiddle
	global original,aligned,detectedImage
	global fileName, faceName
	global embeddings
	global net
	global thresholdValue
	net = TorchNeuralNet()	
	print("obje olustu")
	faceAligned_BGR = cv2.cvtColor(faceAligned_RGB, cv2.COLOR_RGB2BGR)
	saveAlignedImage(faceAligned_BGR)
	embeddings = net.forward(faceAligned_RGB)
	

	print "Array embedding :", embeddings
	stringEmb = ','.join(map(str, embeddings))
	print "stringEmb :", stringEmb
	embeddingNew = stringEmb.split(',')
	print "Array embedding2 :", embeddingNew

	if Database_helper.isFound(embeddings) == False:
		if args["threshold"] == "compute":
			thresholdValue = Database_helper.findThresholdValue(embeddings)
		Database_helper.record(embeddings, faceName)
		print "thresholdValue :", thresholdValue
	else:
		print "Already registered face"
	
	print("faceName2:",faceName)
	
def clickedRecognize():
	global embeddings, net, thresholdValue
	net = TorchNeuralNet()
	faceAligned_BGR = cv2.cvtColor(faceAligned_RGB, cv2.COLOR_RGB2BGR)
	embeddings = net.forward(faceAligned_RGB)
	Database_helper.recognize(embeddings, thresholdValue)	
	
selectImageButton = Button(bottomFrame, text="Select image", fg="red",command = clickedImage)
selectImageButton.pack(side = TOP)
registerButton = Button(bottomFrame, text="Register", fg="black", command = clickedRegister)
registerButton.pack( side = LEFT)
recognizeButton = Button(bottomFrame, text="Recognize", fg="black",command = clickedRecognize)
recognizeButton.pack( side = RIGHT)

window.geometry('500x500')
window.title("Face Recognition")
window.mainloop()

def shape_to_np(shape, dtype="int"):
	# initialize the list of (x, y)-coordinates
	coords = np.zeros((shape.num_parts, 2), dtype=dtype)

	# loop over all facial landmarks and convert them
	# to a 2-tuple of (x, y)-coordinates
	for i in range(0, shape.num_parts):
		coords[i] = (shape.part(i).x, shape.part(i).y)

	# return the list of (x, y)-coordinates
	return coords


