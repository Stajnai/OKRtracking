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
		self.roi1 = None # previously - np.array([0,0]) - trying to see if default value needed
		self.roi2 = None # np.array([0,0]) * see note above ^^
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
	'''
	#fixing personal annoyance of deleting files
	def __del__(self):
			self.outputFileHandle.close()
			os.remove(self.outputFileHandle.name)
	'''
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

		self.writeToFile(7,9)

	def setROI(self):
		roi = cv2.selectROI("Select Region of Interest",self.frame,showCrosshair=False,fromCenter=False)
		self.roi1 = (roi[0],roi[1])
		self.roi2 = (roi[0]+roi[2],roi[1]+roi[3]) # openCv selet returns a rectangle(x,y,width,height)

	def lineTransform(self):

		edge = cv2.Canny(self.frame,self.min,self.max)
		cropImg = edge[self.roi1[1]:self.roi2[1] , self.roi1[0]:self.roi2[0]]

		####################################
		# Classic straight-line Hough transform
		# Set a precision of 0.5 degree.
		tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 360)# This is saying take 360*2 steps from -90 counter cloack wise to +90*(180/np.pi)

		h, theta, d = hough_line(cropImg, theta=tested_angles) # this returns hough transform accumulator, the angles, and distances from orgin to detected line

		# Generating figure 1
		fig, axes = plt.subplots(1, 2, figsize=(15, 6))
		ax = axes.ravel()

		ax[0].imshow(cropImg, cmap=cm.gray)
		ax[0].set_title('Input image')
		ax[0].set_axis_off()

		ax[1].imshow(cropImg, cmap=cm.gray)
		origin = np.array((0, cropImg.shape[1])) #origin considered bottom left

		_, angle, dist = hough_line_peaks(h, theta, d,num_peaks= 4)

		# finding which eye(s) to try to transform the lines for
		if self.eyeNum == -1:
			index = np.where(dist == np.min(dist))
			y0, y1 = (dist[index] - origin * np.cos(angle[index])) / np.sin(angle[index])
			ax[1].plot(origin, (y0, y1),label = "left")
		elif self.eyeNum == 1:
			index = np.where(dist == np.max(dist))
			y0, y1 = (dist[index] - origin * np.cos(angle[index])) / np.sin(angle[index])
			ax[1].plot(origin, (y0, y1),label = "right")
		else:
			minIndex = np.where(dist == np.min(dist))
			maxIndex = np.where(dist == np.max(dist))

			miny0, miny1 = (dist[minIndex] - origin * np.cos(angle[minIndex])) / np.sin(angle[minIndex])
			maxy0, maxy1 = (dist[maxIndex] - origin * np.cos(angle[maxIndex])) / np.sin(angle[maxIndex])

			ax[1].plot(origin, (miny0, miny1),label = "left")
			ax[1].plot(origin, (maxy0, maxy1), label = "right")

		ax[1].set_xlim(origin)
		ax[1].set_ylim((cropImg.shape[0], 0))
		ax[1].set_axis_off()
		ax[1].set_title('Detected lines')
		ax[1].legend()

		plt.tight_layout()
		plt.show()

	def writeToFile(self, leftAngle = 0, rightAngle = 0):

		print("made it to write to file")
		if self.writer == None:
			print("Made it to the column names thing")
			fieldnames = ['leftEye', 'rightEye']
			self.writer = csv.DictWriter(self.outputFileHandle, fieldnames=fieldnames)
			self.writer.writeheader()
		
		self.writer.writerow({'leftEye': leftAngle, 'rightEye': rightAngle})

	def setEyeNum(self,eyeNum):

		eyeNum = int(eyeNum) # take care of decimal answers
		if eyeNum >= -1 and eyeNum <= 1:
			self.eyeNum = eyeNum #for floating points to be discarded
		else:
			raise Exception("Bad eye number indicator")


#proj1 = Project("TestData//LitFishVid.mp4")
#proj1.EdgeDetec()
#retval = cv2.selectROI("testing123", proj1.frame,True, True)
#print(retval)
#proj1.setROI()

proj = Project("TestData//LitFishVid.mp4")

#cv2.imshow("Frame",proj.frame)
proj.writeToFile()

proj.EdgeDetec()
proj.max = 150
proj.min = 100
proj.setROI()
proj.lineTransform()

proj.writeToFile()
proj.writeToFile(1,1)
proj.writeToFile(2,2)
proj.writeToFile(3,4)

proj.outputFileHandle.close