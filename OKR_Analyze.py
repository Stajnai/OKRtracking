# Standard library imports
import csv

# Third party imports
from skimage.filters import sobel
from skimage.segmentation import watershed
from skimage.transform import hough_line, hough_line_peaks
from scipy import ndimage as ndi
import numpy as np
from matplotlib import cm

import cv2
# import matplotlib.pyplot as plt # not used on final product, but used for testing/development

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
		self.min = 0
		self.max = 0
		self.roi1 = None # previously - np.array([0,0]) - trying to see if default value needed
		self.roi2 = None # np.array([0,0]) * see note above ^^
		self.eyeNum = 0
		self.Xnose = 0
		self.Ynose = 0
		self.animationFrame = None

		# Creating input file path and checking by trying to read the first frame
		try:
			ret,self.frame = self.inputVideo.read()
			self.frame = resize(self.frame)
			self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		except:
			raise Exception("There was an error with the input file path.") #another exception is raised by the try for the size error in shape?
			
		# Setting the output file
		try:
			self.outputFileHandle = open('fishAngles.csv', 'x+', newline='')
		except:
			fileNum = 1
			while(self.outputFileHandle == None):
				try:
					self.outputFileHandle = open("fishAngles" + str(fileNum) + ".csv", 'x+',newline = '')
				except:
					self.outputFileHandle = None #is this redundant?
					fileNum += 1
	
	#fixing personal annoyance of deleting files
	def __del__(self):
		self.outputFileHandle.close()
	def getNextFrame(self):
		prevFrame = self.frame # for a try catch?
		ret, self.frame = self.inputVideo.read()
		if ret:
			self.frame = resize(self.frame)
			self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		return ret, self.frame #do i need the self.frame?

	def EdgeDetec(self):
		windowName = "Edge Detection"

		cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)
		#cv2.resizeWindow(windowName,self.frame.shape[1],self.frame.shape[0]+100)

		def setMin(Min) :
			self.min = Min
		def setMax(Max):
			self.max = Max

		cv2.createTrackbar("Max",windowName,0,255,setMin)
		cv2.createTrackbar("Min",windowName,0,255,setMax)

		while cv2.getWindowProperty(windowName, 0) >= 0:# Need to figure out X on fish fig& loopFlag >=0:# and cv2.getWindowProperty('Fish Edges', 0) >= 0):
			
			edge = cv2.Canny(self.frame, self.min, self.max)

			cv2.imshow(windowName, edge)

			if cv2.waitKey(1) & 0xff == ord(' '): #ord returns the unicode of that letter. 0xff makes it only look at 
				#the last 8 bits of the wait key because it is 32bits and the incode is only 8 bits
				break

		cv2.destroyAllWindows()

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
		tested_angles = np.linspace((-np.pi / 2) + (np.pi / 4) , (np.pi / 2) - (np.pi / 4 ), 360)# This is saying take 360*2 steps from -45 counter cloack wise to +45*(180/np.pi)

		h, theta, d = hough_line(cropImg, theta=tested_angles) # this returns hough transform accumulator, the angles, and distances from orgin to detected line

		'''
		# Generating figure 1
		fig, axes = plt.subplots(1, 2, figsize=(15, 6))
		ax = axes.ravel()

		ax[0].imshow(cropImg, cmap=cm.gray)
		ax[0].set_title('Input image')
		ax[0].set_axis_off()

		ax[1].imshow(cropImg, cmap=cm.gray)
		'''
		origin = np.array((0, cropImg.shape[1])) #origin considered bottom left

		_, angle, dist = hough_line_peaks(h, theta, d,num_peaks= 4)

		

		# finding which eye(s) to try to transform the lines for
		minIndex = np.where(dist == np.min(dist))
		maxIndex = np.where(dist == np.max(dist))


		miny0, miny1 = (dist[minIndex][0] - origin * np.cos(angle[minIndex][0])) / np.sin(angle[minIndex][0])
		maxy0, maxy1 = (dist[maxIndex][0] - origin * np.cos(angle[maxIndex][0])) / np.sin(angle[maxIndex][0])

		# The Visuals
		self.animationFrame = cv2.cvtColor(self.frame, cv2.COLOR_GRAY2BGR)

		if self.eyeNum < 0:
			self.animationFrame = cv2.line(self.animationFrame,(self.roi1[0],self.roi1[1] +
			int(miny0)),(self.roi2[0],self.roi2[1] + int(miny1)),(0,255,0), thickness=2)
		elif self.eyeNum > 0:
			self.animationFrame = cv2.line(self.animationFrame,(self.roi1[0],self.roi1[1] +
			int(maxy0)),(self.roi2[0],self.roi2[1] + int(maxy1)),(0,255,255), thickness=2)
		else:
			self.animationFrame = cv2.line(self.animationFrame,(self.roi1[0],self.roi1[1] +
			int(miny0)),(self.roi2[0],self.roi2[1] + int(miny1)),(0,255,0), thickness=2)

			self.animationFrame = cv2.line(self.animationFrame,(self.roi1[0],self.roi1[1] +
			int(maxy0)),(self.roi2[0],self.roi2[1] + int(maxy1)),(0,255,255), thickness=2)

		cv2.imshow("Lines", self.animationFrame)
		cv2.waitKey(1)
		'''			
		ax[1].plot(origin, (miny0, miny1),label = "left")
		ax[1].plot(origin, (maxy0, maxy1), label = "right")
		
		ax[1].set_xlim(origin)
		ax[1].set_ylim((cropImg.shape[0], 0))
		ax[1].set_axis_off()
		ax[1].set_title('Detected lines')
		ax[1].legend()

		plt.tight_layout()
		#plt.show()
		'''

		retval = [0,0]
		if self.eyeNum == -1:
			retval[0] = angle[minIndex][0]
		elif self.eyeNum == 1:
			retval[1] = angle[maxIndex][0]
		else:
			retval[0] = angle[minIndex][0]
			retval[1] = angle[maxIndex][0]

		return retval

	def writeToFile(self, Angles = [0,0]):

		leftAngle =  Angles[0]
		rightAngle = Angles[1]

		if self.writer == None:
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

	def findFishNose(self):
		markers = np.zeros_like(self.frame)
		markers[self.frame < 30] = 2  # these just work
		markers[self.frame > 150] = 1 # these just work
	
		elevation_map = sobel(self.frame)
		segmentation = watershed(elevation_map, markers)
		segmentation = ndi.binary_fill_holes(segmentation - 1) # I believe this sets that background as 0 so we don't change it
		labeled_img, num_features = ndi.label(segmentation)

		freq = np.argmax(np.bincount(labeled_img.flatten())[1:]) + 1
		
		index = np.where(labeled_img == freq)

		self.Ynose = index[0][0]
		self.Xnose = index[1][index[0] == self.Ynose]
		
		def findMed(arr):
			return arr[int(np.trunc(len(arr)/2))]
		
		self.Xnose = findMed(self.Xnose)

	def adjustROI(self):

		if(self.Xnose == 0 and self.Ynose == 0):
			print("This is an exception")

		roi1dif = (self.roi1[0] - self.Xnose , self.roi1[1] - self.Ynose)
		roi2dif = (self.roi2[0] - self.Xnose , self.roi2[1] - self.Ynose)

		self.findFishNose()
		self.roi1 = (roi1dif[0] + self.Xnose, roi1dif[1] + self.Ynose)
		self.roi2 = (roi2dif[0] + self.Xnose, roi2dif[1] + self.Ynose)

	def autoAnalyzeVideo(self):
		'''
		#checks
		self.findFishNose()
		#eye num is set in the GUI
		while self.roi1 == None or self.roi2 == None:
			print("Please set the region of interest")
			self.setROI()
			#self.roi1 = (134,111)
			#self.roi2 = (246,163)

		while self.min == 0 and self.max == 0: # I'm concerned about this boolean not checking both???????????????????????????????????
			print("Please set the edge detection max and min values")
			self.EdgeDetec()
			#self.max = 153
			#self.min = 51
		'''

		while self.getNextFrame()[0]:
			self.adjustROI()
			self.writeToFile(self.lineTransform())
		