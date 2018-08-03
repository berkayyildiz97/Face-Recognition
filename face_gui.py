# USAGE
# python cat_detector.py --image images/cat_01.jpg

# import the necessary packages
import argparse
import cv2
import dlib
import numpy as np
import FaceAligner
import align_dlib
from PIL import Image
from PIL import ImageTk

def shape_to_np(shape, dtype="int"):
    # initialize the list of (x, y)-coordinates
    coords = np.zeros((shape.num_parts, 2), dtype=dtype)

    # loop over all facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, shape.num_parts):
        coords[i] = (shape.part(i).x, shape.part(i).y)

    # return the list of (x, y)-coordinates
    return coords

def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized

def startDetection(fileName):
	shape_predictor = "shape_predictor_68_face_landmarks.dat"
	# construct the argument parse and parse the arguments
	'''
	ap = argparse.ArgumentParser()
	ap.add_argument("-c", "--cascade",
		        default="haarcascade_frontalface_default.xml",
		        help="path to face detector haar cascade")
	# ap.add_argument("-p", "--shape-predictor", required=True,
	#	help="path to facial landmark predictor")
	args = vars(ap.parse_args())

	'''
	# load the input image and convert it to grayscale
	image = cv2.imread(fileName)
	heightO, widthO, channelsO = image.shape 
	print("original width,height=" , widthO,heightO)
	#image = resize(image, width=500,height= 500)
	
	#image = cv2.resize(image, (100, 100)) 
 
	#  Image to array (Biz ekledik)
	# savefig('rihanna.jpg')
	#
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	image_return = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	image_return = Image.fromarray(image_return)
	image_return = ImageTk.PhotoImage(image_return)

	# load the cat detector Haar cascade, then detect cat faces
	# in the input image
	detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	#default scale factor = 1.3,1.04 de iyi
	
	rects = detector.detectMultiScale(gray, scaleFactor=1.2,minNeighbors=10, minSize=(75, 75))
	i=0.01
	while True:
		if len (rects)!=0:
			print(1.2-i)
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
	##fa = FaceAligner.FaceAligner(predictor, desiredFaceWidth=96)
	fa = align_dlib.AlignDlib(shape_predictor)

	# loop over the face detections

	faceAligned_RGB = None
	faceAligned_return = None
	
	for (i, rect) in enumerate(rects):
	    # determine the facial landmarks for the face region, then
	    # convert the facial landmark (x, y)-coordinates to a NumPy
	    # array
	    print(rect)
	    x = rect[0]
	    y = rect[1]
	    w = rect[2]
	    h = rect[3]

	    rect = dlib.rectangle(x, y, x + w, y + h)
	    print(rect)
	    shape = predictor(gray, rect)
	    shape = shape_to_np(shape)
	    #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
	    #cv2.putText(image, "Face #{}".format(i + 1), (x, y - 10),
		        #cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
	    # loop over the (x, y)-coordinates for the facial landmarks
	    # and draw them on the image

	    # Face Normalization   
	    ##faceAligned = fa.align(image, gray, rect)
	    faceAligned = fa.align(96, image)
	    if faceAligned is None:
		continue
	    height, width, channels = faceAligned.shape 
	    print("aligned width,height=" , width,height)
	    faceAligned_return = cv2.cvtColor(faceAligned, cv2.COLOR_BGR2RGB)
	    faceAligned_RGB = faceAligned_return
	    
	    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
	    cv2.putText(image, "Face #{}".format(i + 1), (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
	    
	    ##ADAMIN FACEALIGNED PENCERESINDE BOX YANA KAYIYOR X VE Y DEGISTIGI ICIN
	    #cv2.rectangle(faceAligned, (x, y), (x + w, y + h), (0, 0, 255), 2)
	    #cv2.putText(faceAligned, "Face #{}".format(i + 1), (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
	    i = 1
	    for (x, y) in shape:
		#print((i, (x, y)))
		# cv2.putText(image, "{}".format(i), (x, y - 10),
		# cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 200, 255), 1)
		i = i + 1
		cv2.circle(image, (x, y), 1, (0, 0, 255), -1)
	
	# show the detected faces
	#cv2.imshow("Aligned", faceAligned)
	#cv2.imshow("Face", image)
	if faceAligned_return is not None:
		faceAligned_return = Image.fromarray(faceAligned_return)
		faceAligned_return = ImageTk.PhotoImage(faceAligned_return)
	
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	image = Image.fromarray(image)
	image = ImageTk.PhotoImage(image)
	
	#cv2.waitKey(0)
	return (image_return,faceAligned_return,image,faceAligned_RGB)
