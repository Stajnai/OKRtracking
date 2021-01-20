import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

import cv2
from skimage.transform import hough_line, hough_line_peaks

import os.path
from os import path
import csv


class Project:

	#codec to output the file
	fourcc = cv2.VideoWriter_fourcc(*'XVID') #this is saying we want to use xvid as our codec
	
	#initializes the instance of a Project
	def __init__(self,inputFilePath):
		
		#The class attributes
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

		#check the input file path by trying to read the first frame
		try:
			ret,self.frame = self.inputVideo.read()
			self.frame = resize(self.frame)
			self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		except:
			self.inputFilePath = None
			print("There was an error with the input file path.")

	
		## setting output file
		if self.inputFilePath != None: #I don't want to create an output if input was bad
			try:
				self.outputFileHandle = open('fishAngles.csv', 'x', newline='')
			except:
				self.outputFileHandle = None #is this redundant?

			fileNum = 1
			while(self.outputFileHandle == None):
				try:
					self.outputFileHandle = open("fishAngles" + str(fileNum) + ".csv", 'x',newline = '')
				except:
					self.outputFileHandle = None #is this redundant?
					fileNum += 1
	

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

	def setROI(self):

		windowName = "ROI"
		
		def setROIHelper(event,x,y,flags,param):

			img = (self.frame).copy()
			if np.equal(self.roi1,np.array([0,0])).all():
				cv2.putText(img,"Select UPPER LEFT bounds of the eyes.",(5,15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),1)
			else:
				cv2.putText(img,"Select LOWER RIGHT bounds of the eyes.",(5,15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)

			if event == cv2.EVENT_MOUSEMOVE:

				if np.not_equal(self.roi1,np.array([0,0])).all() and np.equal(self.roi2,np.array([0,0])).all(): #if the first selection made and the second isnt
					cv2.rectangle(img,(self.roi1[0],self.roi1[1]),(x,y),(255,255,0),2)

				elif np.not_equal(self.roi2,np.array([0,0])).all(): #if second selection made
					cv2.rectangle(img,(self.roi1[0],self.roi1[1]),(self.roi2[0],self.roi2[1]),(255,255,0),2)
					
				cv2.imshow(windowName,img)

			if event == cv2.EVENT_LBUTTONDOWN:
				if np.equal(self.roi1,np.array([0,0])).all():
					self.roi1[0] = x
					self.roi1[1] = y
				else:
					self.roi2[0] = x
					self.roi2[1] = y
					return
	
		#end helper
		cv2.imshow(windowName,self.frame) #this creates the window we will be working on too!!!
		cv2.setMouseCallback(windowName,setROIHelper)

		while cv2.getWindowProperty(windowName, 0) >= 0:
			# display the image and wait for a keypress
			key = cv2.waitKey(1) & 0xFF
			# if the 'r' key is pressed, reset the cropping region
			if key == ord("r"):
				self.roi1 = np.array([0,0])
				self.roi2 = np.array([0,0])
				img = (self.frame).copy()
				cv2.putText(img,"Select UPPER LEFT bounds of the eyes.",(5,15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),1)
				cv2.imshow(windowName,img)
			# if the 'c' key is pressed, break from the loop
			elif key == ord("d"):
				cv2.destroyAllWindows()
				#print(self.roi1[1],self.roi2[1] , self.roi1[0],self.roi2[0])

		return
	#end setROI

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
		origin = np.array((0, cropImg.shape[1])) #bottom left

		_, angle, dist = hough_line_peaks(h, theta, d,num_peaks= 4)

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

		if self.writer == None:
			fieldnames = ['leftEye', 'rightEye']
			self.writer = writer = csv.DictWriter(self.outputFileHandle, fieldnames=fieldnames)
			self.writer.writeheader()
		
		self.writer.writerow({'leftEye': leftAngle, 'rightEye': rightAngle})

	def setEyeNum(self,eyeNum):
		if eyeNum >= -1 and eyeNum <= 1:
			self.eyeNum = int(eyeNum) #for floating points to be discarded
		else:
			print("Bad eye number indicator")

### separate??
def resize(img):
	height,width,__ = img.shape ## Need the blank variable or else "TypeError: argument 1 must have a "write" method"

	scale_percent = 512 / width
	width = int(img.shape[1] * scale_percent) #python makes it a float, and it needs an int
	height = int(img.shape[0] * scale_percent)
	img = cv2.resize(img,(width,height),interpolation = cv2.INTER_AREA)

	return img

	# #this is the "main" function
SofsProject = Project("TestData//LitFishVid.mp4")
	
	# #cv2.imshow("Frame",SofsProject.frame)
	# #SofsProject.EdgeDetec()
	# #SofsProject.setROI()
	# #SofsProject.lineTransform()

	# SofsProject.writeToFile()
	# SofsProject.writeToFile(1,1)
	# SofsProject.writeToFile(2,2)
	# SofsProject.writeToFile(3,4)

	# SofsProject.setEyeNum(0)
	# SofsProject.EdgeDetec()
SofsProject.setROI()
print(SofsProject.roi1, SofsProject.roi2)
	# SofsProject.lineTransform()

	# cv2.waitKey(0)
	# cv2.destroyAllWindows()