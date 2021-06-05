import numpy as np
import cv2

from skimage.transform import hough_line, hough_line_peaks
from skimage.feature import canny
from skimage import data

import matplotlib.pyplot as plt
from matplotlib import cm

def resize(img):
	height,width = img.shape
	
	while (height > 800 or width > 800):
		scale_percent = 0.95
		width = int(img.shape[1] * scale_percent) #python makes it a float, and it needs an int
		height = int(img.shape[0] * scale_percent)
		img = cv2.resize(img,(width,height),interpolation = cv2.INTER_AREA)
	return img


#img = cv2.imread(".//TestData//LitFish.png",cv2.COLOR_BGR2GRAY)
img = cv2.imread(".//TestData//Left.png",cv2.COLOR_BGR2GRAY)
#plt.imshow(image) #you have to plot
#plt.show()		  #and then show

img = resize(img)


#Necessary variables for trackabrs
cv2.namedWindow("Canny Edge")
def onTrack(x) :
	pass

cv2.createTrackbar("Max","Canny Edge",0,255,onTrack)
cv2.createTrackbar("Min","Canny Edge",0,255,onTrack)

loopFlag = 1
mx = 0
mn = 0
edge = img
while cv2.getWindowProperty('Canny Edge', 0) >= 0 :# Need to figure out X on fish fig& loopFlag >=0:# and cv2.getWindowProperty('Fish Edges', 0) >= 0):
	
	mx = cv2.getTrackbarPos("Max","Canny Edge")
	mn = cv2.getTrackbarPos("Min","Canny Edge")
	edge = cv2.Canny(img,mn,mx)

	#loopFlag = cv2.getWindowProperty('Fish Edges', 0)

	cv2.imshow("Fish Edges",edge)

	if cv2.waitKey(1) & 0xff == ord('q') or cv2.waitKey(1) & 0xff == ord('d'): #ord returns the unicode of that letter. 0xff makes it only look at 
		#the last 8 bits of the wait key because it is 32bits and the incode is only 8 bits
		break

#print(mx, mn)
cv2.destroyAllWindows()

#plt.imshow(img) #you have to plot
#plt.show()		  #and then show

cropImg = edge[150:324,200:471] #Y,X because rows, columns
#plt.imshow(cropImg)
#plt.show()



####################################
# Classic straight-line Hough transform
# Set a precision of 0.5 degree.
tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 360)# This is saying take 360*2 steps from -90 counter cloack wise to +90*(180/np.pi)

h, theta, d = hough_line(cropImg, theta=tested_angles) # this returns hough transform accumulator, the angles, and distances from orgin to detected line
#plt.plot(h,'o')
#plt.show()
#print(theta)
#print()
#print(d)  # I MIGHT WANT TO CONSIDER USING D AS A PARAMETER


# Generating figure 1
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
ax = axes.ravel()

ax[0].imshow(cropImg, cmap=cm.gray)
ax[0].set_title('Input image')
ax[0].set_axis_off()

ax[1].imshow(cropImg, cmap=cm.gray)
origin = np.array((0, cropImg.shape[1])) #bottom left
lab = 1
for _, angle, dist in zip(*hough_line_peaks(h, theta, d,num_peaks= 10)): # the angles are base off of the y axis??
	#print("origin" + str(lab),origin)
	print("angle" + str(lab),angle*(180/np.pi))
	y0, y1 = (dist - origin * np.cos(angle)) / np.sin(angle)
	print("yvalues" + str(lab),y0,y1)
	print("distance"+str(lab),dist)
	print()
	ax[1].plot(origin, (y0, y1), '-o',color = "C" + str(lab),label = str(lab))
	lab +=1

ax[1].set_xlim(origin)
ax[1].set_ylim((cropImg.shape[0], 0))
ax[1].set_axis_off()
ax[1].set_title('Detected lines')
ax[1].legend()

plt.tight_layout()
plt.show()
