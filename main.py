import numpy as np
import cv2
import os.path
from os import path

#notes for sof - attricbutes are lowercase and methods are capital
#A project is created for any video analysis and requires a valid filepath to create
class Project:

	#codec to output the file
	fourcc = cv2.VideoWriter_fourcc(*'XVID') #this is saying we want to use xvid as our codec
	
	#initializes the instance of a Project
	def __init__(self,inputFilePath):
		
		#The class attributes
		self.inputVideo = cv2.VideoCapture(inputFilePath)
		self.inputFilePath = inputFilePath
		self.outputFilePath = "OKRtracking.avi" #os.path.expanduser("~")+"//Downloads//"   <-- this is for downloads?
		self.fps = 20.0
		self.ratio = None #(width,height) is the convention
		self.outputVideo = None
		self.frame = None #place holder
		

		#check the input file path by trying to read the first frame
		try:
			ret,self.frame = self.inputVideo.read()
			height, width, channels = self.frame.shape 
			self.ratio = (width,height)
			self.outputVideo = cv2.VideoWriter(self.outputFilePath, Project.fourcc, self.fps, self.ratio) #this is saying what our output file is
		except:
			self.inputFilePath = None
			print("There was an error with the input file path.")

	#sets the input file path
	def setInputFilePath(self,inputFilePath):
		#maybe only allow this if inputFilePath == None? can't change for project
		try:
			self.inputFilePath = inputFilePath
			self.inputVideo = cv2.VideoCapture(inputFilePath)
			ret,self.frame = self.inputVideo.read()
			height, width, channels = self.frame.shape 
			self.ratio = (width,height)
			#maybe not do this here for orgnization?#self.outputVideo = cv2.VideoWriter(self.outputFilePath, Project.fourcc, self.fps, self.ratio) #this is saying what our output file is
		except:
			print("There was an error with the input file path.")

	#sets the output file path and updates the output video codec function
	def setOutputFilePath(self,outputFilePath):
		self.outputFilePath = outputFilePath
		#self.outputVideo = cv2.VideoWriter(self.outputFilePath, Project.fourcc, self.fps, self.ratio) #this is saying what our output file is
		if path.exists(outputFilePath) == False:
			self.outputFilePath = "OKRtracking.avi"
			self.outputVideo = cv2.VideoWriter(self.outputFilePath, Project.fourcc, self.fps, self.ratio) #this is saying what our output file is
			print("There was an error with the output file path")

	
	#returns true or false if a frame is read and update the self.frame attribute
	def getFrame(self):
		prevFrame = self.frame
		ret, self.frame = self.inputVideo.read()
		return ret, self.frame #do i need the self.frame?


#this is the "main" function
SofsProject= Project("hello")#"TestData//stillFish.mp4")
SofsProject.setInputFilePath("TestData//stillFish.mp4")
#.imshow("fish",SofsProject.frame)
if SofsProject.getFrame():
	cv2.imshow("fish",SofsProject.frame)

SofsProject.setOutputFilePath("testWrite.mp4") #for some reason it outputs two files if outputfil
SofsProject.setOutputFilePath("testWriteCheck.mp4") #for some reason it outputs two files if outputfil

#'''
while SofsProject.getFrame()[0]:
	SofsProject.outputVideo.write(SofsProject.frame)

SofsProject.inputVideo.release()
SofsProject.outputVideo.release()
#'''
cv2.waitKey(0)
cv2.destroyAllWindows()