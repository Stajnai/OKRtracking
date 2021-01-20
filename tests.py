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
	assert all(proj1.roi1) == all(np.array([0,0]))
	assert all(proj1.roi2) == all(np.array([0,0]))
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

def test_
### Notes
'''
pytest -rP will show the outputs after the test results
'''