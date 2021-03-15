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

img = cv2.imread("TestData//Left.png",cv2.COLOR_BGR2GRAY)
img = resize(img)

ret,thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
cv2.imshow("Thresh",thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

#print(img)

'''
x = np.array([[1,2,3],
		      [4,5,6],
	    	  [7,8,9]])
print(x[0,:])
'''

x = 25
maxBlack = 0
#for line in range(x):
	





'''
height,width = img.shape

crop = thresh[0:height   ,   (int((width/2))-100)  :  (int((width/2))+100)]
cv2.imshow("crop",crop)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
