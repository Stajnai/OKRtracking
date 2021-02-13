# Standard library imports
import os
import csv

# Third party imports
import cv2
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pytest
from skimage.transform import hough_line, hough_line_peaks

# Local application imports
import newmain as okr

@pytest.fixture
def proj1():

	proj1 = okr.Project("TestData//LitFishVid.mp4")

	yield proj1
	proj1.outputFileHandle.close()
	os.remove(proj1.outputFileHandle.name)

def test_init(proj1):

	#The class attributes
	assert proj1.inputFilePath == "TestData//LitFishVid.mp4"
	assert proj1.inputVideo.isOpened() == True
	assert proj1.outputFileHandle != None
	assert proj1.writer == None
	assert len(proj1.frame.shape) == 2 # this means the try..except for input file worked!
	assert proj1.max == 0
	assert proj1.min == 0
	assert proj1.roi1 == None #all(proj1.roi1) == all(np.array([0,0]))
	assert proj1.roi2 == None #all(proj1.roi2) == all(np.array([0,0]))
	assert proj1.eyeNum == 0

def test_resize(proj1):

	# default resize
	img = okr.resize(proj1.frame)
	assert img.shape[1]==512

	# resize to larger
	img = okr.resize(img,1024)
	assert img.shape[1] == 1024

	# resize to smaller
	img = okr.resize(img,256)
	assert img.shape[1] == 256

def test_getNextFrame(proj1):

	frame1 = proj1.frame
	ret, frame2 = proj1.getNextFrame()

	# This does not work with the still image video :(
	#if ret: 
		#assert frame1.all() != frame2.all()

	if not ret:
		assert frame2 == None

	ret = True
	while ret:
		ret,frame3 = proj1.getNextFrame()
	assert frame3 == None

def test_EdgeDetec(proj1):
	# not sure how to test this?
	True

def test_setROI(proj1):

	# not quite sure how to test this?  gui components? 
	proj1.setROI()
	assert proj1.roi1 != None
	assert proj1.roi2 != None
	
def test_lineTransform(proj1):
	# not sure how to test this one yet.
	True

def test_writeToFile(proj1):
	
	# write to file
	proj1.writeToFile() #test defaults
	proj1.writeToFile([1,0])
	proj1.writeToFile([0,2])
	proj1.writeToFile([3,4])

	# close file and open in read mode
	proj1.outputFileHandle.close()
	fh = open(proj1.outputFileHandle.name,'r')
	contents = fh.readlines()

	assert contents[0] == "leftEye,rightEye\n"
	assert contents[1] == "0,0\n"
	assert contents[2] == "1,0\n"
	assert contents[3] == "0,2\n"
	assert contents[4] == "3,4\n"

def test_setEyeNum(proj1):

	# non exceptions
	proj1.setEyeNum(-1)
	assert proj1.eyeNum == -1

	proj1.setEyeNum(0)
	assert proj1.eyeNum == 0

	proj1.setEyeNum(1)
	assert proj1.eyeNum == 1
	
	proj1.setEyeNum(0.5)
	assert proj1.eyeNum == 0

	# exceptions to be raised

	with pytest.raises(Exception):
		proj1.setEyeNum(-500)
	
	with pytest.raises(Exception):
		proj1.setEyeNum(500)

	with pytest.raises(Exception):
		proj1.setEyeNum(50.5)
'''
def test_AllFunctionsAtOnce():
	proj = okr.Project("TestData//LitFishVid.mp4")

	cv2.imshow("Frame",proj.frame)
	proj.writeToFile()

	
	#proj.EdgeDetec()# # WHY IS THIS NOT ALLOWING TO WRITE TO FILE???!!!!!?????!!!!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!
	proj.setROI()
	proj.max = 150
	proj.min = 80
	proj.lineTransform()

	proj.writeToFile()
	proj.writeToFile(1,1)
	proj.writeToFile(2,2)
	proj.writeToFile(3,4)

	#proj.setEyeNum(0)
	#proj.EdgeDetec()
	#proj.setROI()
	#print(proj.roi1, proj.roi2)
	#proj.lineTransform()

	cv2.waitKey(0)
	cv2.destroyAllWindows()

'''
### Notes
'''
"pytest -rP .\filename" will show the outputs after the test results
'''