import numpy as np
import cv2
import matplotlib as plt
import os.path
from os import path

class Project:

	#codec to output the file
	fourcc = cv2.VideoWriter_fourcc(*'XVID') #this is saying we want to use xvid as our codec
	
	#initializes the instance of a Project
	def __init__(self,inputFilePath):
		
		#The class attributes
		self.inputFilePath = inputFilePath
		self.inputVideo = cv2.VideoCapture(inputFilePath)
		self.frame = None
		self.max = 0
		self.min = 0		

		#check the input file path by trying to read the first frame
		try:
			ret,self.frame = self.inputVideo.read()
			self.frame = resize(self.frame)
			self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		except:
			self.inputFilePath = None
			print("There was an error with the input file path.")

	
	#returns true or false if a frame is read and update the self.frame attribute
	def getNextFrame(self):
		prevFrame = self.frame # for a try catch?
		ret, self.frame = self.inputVideo.read()
		self.frame = resize(self.frame)
		self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		return ret, self.frame #do i need the self.frame?

	def EdgeDetec(self):
		
		windowName = "Edge Detection"
		cv2.namedWindow(windowName)
		def onTrack(x) :
			pass

		cv2.createTrackbar("Max",windowName,0,255,onTrack)
		cv2.createTrackbar("Min",windowName,0,255,onTrack)

		loopFlag = 1
		edge = self.frame #Needs to be here to allow higher scope
		while cv2.getWindowProperty(windowName, 0) >= 0 :# Need to figure out X on fish fig& loopFlag >=0:# and cv2.getWindowProperty('Fish Edges', 0) >= 0):
			
			self.max = cv2.getTrackbarPos("Max",windowName)
			self.min = cv2.getTrackbarPos("Min",windowName)
			edge = cv2.Canny(self.frame, self.min, self.max)

			#loopFlag = cv2.getWindowProperty('Fish Edges', 0)

			cv2.imshow("Fish Edges",edge)

			if cv2.waitKey(1) & 0xff == ord('q') or cv2.waitKey(1) & 0xff == ord('d'): #ord returns the unicode of that letter. 0xff makes it only look at 
				#the last 8 bits of the wait key because it is 32bits and the incode is only 8 bits
				break

		#print(self.max, self.min)
		cv2.destroyAllWindows()

### separate??
def resize(img):
	height,width, _ = img.shape
	
	while (height > 1000 or width > 1000):
		scale_percent = 0.95
		width = int(img.shape[1] * scale_percent) #python makes it a float, and it needs an int
		height = int(img.shape[0] * scale_percent)
		img = cv2.resize(img,(width,height),interpolation = cv2.INTER_AREA)
	return img


#this is the "main" function
SofsProject = Project("TestData//LitFishVid.mp4")


#cv2.imshow("Frame",SofsProject.frame)
SofsProject.EdgeDetec()


cv2.waitKey(0)
cv2.destroyAllWindows()