import cv2,os
import numpy as np
from PIL import Image

#recognizer = cv2.createLBPHFaceRecognizer()
recognizer = cv2.face.LBPHFaceRecognizer_create ();
detector= cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

def getImagesAndLabels(path):
	#get the path of all the files in the folder
	directoryPaths=[os.path.join(path,f) for f in os.listdir(path)]
	#print imagePaths	
	#create empth face list
	faceSamples=[]
	#create empty ID list
	Ids=[]
	#now looping through all the image paths and loading the Ids and the images
	index = 0 		
	dictionary = {}
	file = open("dictionary.txt","w")
	for root, directories, filenames in os.walk('/home/berkay/FaceRecog2/lfw'):
		directoryId = ""
		for imagePath in filenames:
			print imagePath
			Id = imagePath[:imagePath.rfind('_')]
			if directoryId != Id:
				index =index+1
				directoryId = Id
				file.write(str(index) +"\t"+ Id+"\n")
			#print "Id: ", Id
			#print "Index: ", index
			dictionary[index] = Id
			#print dictionary
			
			#loading the image and converting it to gray scale
			imagePath = os.path.join(root,imagePath)
			#print "after join :", imagePath
			pilImage=Image.open(imagePath).convert('L')
			#Now we are converting the PIL image into numpy array
			imageNp=np.array(pilImage,'uint8')
			#getting the Id from the image
			#print Id
			# extract the face from the training image sample
			faces=detector.detectMultiScale(imageNp)
			#If a face is there then append that in the list as well as Id of it
			for (x,y,w,h) in faces:
				faceSamples.append(imageNp[y:y+h,x:x+w])
				Ids.append(index)
	return faceSamples,Ids



faces,Ids = getImagesAndLabels('lfw')
print "IDs: ", Ids
recognizer.train(faces, np.array(Ids))
