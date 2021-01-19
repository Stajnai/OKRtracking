# Standard library imports
import os # ?? may not be needed with the next line
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

	#create a project
	#proj1 = okr.Project("TestData//LitFishVid.mp4")
	'''
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
	'''
	print("test1")


def test_resize(proj1):
	'''
	img = okr.resize(proj1.frame)
	assert img.shape[1]==512
	#print(proj1.frame.shape)
	'''
	print("test2")


### Notes
'''
pytest -rP will show the outputs after the test results
'''