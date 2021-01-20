# Standard library imports
import os
import csv

# Third party imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

from skimage.transform import hough_line, hough_line_peaks
import cv2

# Local application imports
# /None


############################## Helper Functions ########################

def resize(img,desiredWidth = 512):
	'''
	Returns a resized copy of the image. Default width is 512.
	'''

	try:
		height,width,__ = img.shape ## Need the blank variable or else "TypeError: argument 1 must have a "write" method"
	except ValueError:
		try:
			height,width = img.shape ## Need the blank variable or else "TypeError: argument 1 must have a "write" method"
		except:
			raise Exception("Failure to unpack image shape.")


	scale_percent = desiredWidth / width
	width = int(img.shape[1] * scale_percent) #python makes it a float, and it needs an int
	height = int(img.shape[0] * scale_percent)
	img = cv2.resize(img,(width,height),interpolation = cv2.INTER_AREA)

	return img

########################################################################
class Project:

	#codec to output the file
	fourcc = cv2.VideoWriter_fourcc(*'XVID') #this is saying we want to use xvid as our codec
	
	#initializes the instance of a Project
	def __init__(self,inputFilePath):

		self.inputFilePath = inputFilePath
		self.inputVideo = cv2.VideoCapture(inputFilePath)
		self.outputFileHandle = None
		self.writer = None
		self.frame = None
		self.max = 0
		self.min = 0
		self.roi1 = np.array([0,0])
		self.roi2 = np.array([0,0])
		self.eyeNum = 0

		# Creating input file path and checking by trying to read the first frame
		try:
			ret,self.frame = self.inputVideo.read()
			self.frame = resize(self.frame)
			self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		except:
			raise Exception("There was an error with the input file path.") #another exception is raised by the try for the size error in shape?
			
		# Setting the output file
		try:
			self.outputFileHandle = open('fishAngles.csv', 'x', newline='')
		except:
			fileNum = 1
			while(self.outputFileHandle == None):
				try:
					self.outputFileHandle = open("fishAngles" + str(fileNum) + ".csv", 'x',newline = '')
				except:
					self.outputFileHandle = None #is this redundant?
					fileNum += 1
	
	#fixing personal annoyance of deleting files
	def __del__(self):
			self.outputFileHandle.close()
			os.remove(self.outputFileHandle.name)

	def getNextFrame(self):
		prevFrame = self.frame # for a try catch?
		ret, self.frame = self.inputVideo.read()
		if ret:
			self.frame = resize(self.frame)
			self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		return ret, self.frame #do i need the self.frame?

	def EdgeDetec(self):
		windowName = "Edge Detection"

		cv2.startWindowThread()
		cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
		#cv2.resizeWindow(windowName,self.frame.shape[1],self.frame.shape[0]+100)

		def setMin(Min) :
			self.min = Min
		def setMax(Max):
			self.max = Max

		cv2.createTrackbar("Max",windowName,0,255,setMin)
		cv2.createTrackbar("Min",windowName,0,255,setMax)

		while cv2.getWindowProperty(windowName, 0) >= 0:# Need to figure out X on fish fig& loopFlag >=0:# and cv2.getWindowProperty('Fish Edges', 0) >= 0):
			
			edge = cv2.Canny(self.frame, self.min, self.max)

			cv2.imshow("Image",edge)

			if cv2.waitKey(1) & 0xff == ord('q') or cv2.waitKey(1) & 0xff == ord('d'): #ord returns the unicode of that letter. 0xff makes it only look at 
				#the last 8 bits of the wait key because it is 32bits and the incode is only 8 bits
				break

		cv2.destroyAllWindows()

	def setROI(self):
		roi = cv2.selectROI("Select Region of Interest",self.frame,showCrosshair=False,fromCenter=False)
		self.roi1 = (roi[0],roi[1])
		self.roi2 = (roi[0]+roi[2],roi[1]+roi[3]) # openCv selet returns a rectangle(x,y,width,height)
		print(self.roi1)
		print(self.roi2)

		img = self.frame
		cv2.circle(img,self.roi1,2,(255,0,0), -1)
		cv2.circle(img,self.roi2,2,(0,255,0), -1)

		cv2.imshow("check",img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()






proj1 = Project("TestData//LitFishVid.mp4")
#proj1.EdgeDetec()
#retval = cv2.selectROI("testing123", proj1.frame,True, True)
#print(retval)
proj1.setROI()