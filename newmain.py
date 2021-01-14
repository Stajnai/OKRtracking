# Standard library imports
#import os.path ?? may not be needed with the next line
from os import path
import csv

# Third party imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

from skimage.transform import hough_line, hough_line_peaks
import cv2

# Local application imports
# /None


#### GLOBAL VARIABLES ###
IMG_SIZE = 512

############################## Helper Functions ########################
def resize(img):
	height,width,__ = img.shape ## Need the blank variable or else "TypeError: argument 1 must have a "write" method"

	scale_percent = IMG_SIZE / width
	width = int(img.shape[1] * scale_percent) #python makes it a float, and it needs an int
	height = int(img.shape[0] * scale_percent)
	img = cv2.resize(img,(width,height),interpolation = cv2.INTER_AREA)

	return img

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
