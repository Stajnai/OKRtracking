import numpy as np
import cv2

#notes for sof - attricbutes are lowercase and methods are capital
#A project is created for any video analysis and requires a valid filepath to create
class Project:

	def __init__(self,inputFilePath):
		
		#set the basics
		self.video = cv2.VideoCapture(inputFilePath)
		self.inputFilePath = inputFilePath

		#try to read the first frame to check path
		try:
			ret,self.frame = self.video.read()
		except:
			self.inputFilePath = None
			print("There was an error with the input file path.")


#this is the "main" function
SofsProject= Project("TestData//stillFish.mp4")
cv2.imshow("fish",SofsProject.frame)
cv2.waitKey(0)
cv2.destroyAllWindows()