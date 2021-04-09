from skimage import data
from skimage.exposure import histogram
from skimage.filters import sobel
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from scipy import ndimage as ndi
import numpy as np
from skimage.feature import canny
import matplotlib.pyplot as plt
import cv2

'''
img = cv2.imread("TestData//Left.png",cv2.COLOR_BGR2GRAY)
#img = resize(img)

ret,thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
#cv2.imshow("Thresh",thresh)
'''

coins = cv2.imread("TestData//Left.png",cv2.COLOR_BGR2GRAY)

markers = np.zeros_like(coins)
markers[coins < 30] = 2
markers[coins > 150] = 1
#markers[coins.any() > 150 and coins.any() < 250] = 1  # 1's are what we want
#markers[coins > 30 and coins < 100] = 3

'''
plt.imshow(markers,cmap = 'gray')
plt.title("Markers")
plt.show()
'''


ax = plt.figure(figsize=(9, 6))

plt.subplot(221)
plt.imshow(markers,cmap = 'gray')
plt.title("Markers")

elevation_map = sobel(coins)

plt.subplot(222)
plt.imshow(elevation_map,cmap = "gist_earth")
plt.title("Elevation Map")

segmentation = watershed(elevation_map, markers)

'''
plt.subplot(233)
plt.imshow(segmentation)
plt.title("Seg 1")
'''
segmentation = ndi.binary_fill_holes(segmentation - 1) # I believe this sets that background as 0 so we don't change it

'''
plt.subplot(233)
plt.imshow(segmentation)
plt.title("Segment w/ Filled Holes")
'''
labeled_coins, num_features = ndi.label(segmentation)

print(num_features)

test = labeled_coins

plt.subplot(223)
plt.imshow(labeled_coins)
#plt.legend((line1,line2),("Labeled","Background"),loc = "upper left"  )
plt.title("Labeled Objects")


freq = np.argmax(np.bincount(test.flatten())[1:]) + 1

#print(freq)

index = np.where(test == freq)

#print(index)

y = index[0][0]
x = index[1][index[0] == y]

print(x)
def findMed(arr):
	return arr[int(np.trunc(len(arr)/2))]

x = findMed(x)

print("Y is: ",y)
print("X is: ",x)

print(test[y][x])

plt.subplot(224)
plt.imshow(test)
plt.title("Final")
plt.arrow(x+200,y-200,-175,175, length_includes_head = True,head_width = 50, linewidth = 3, color = "r")
plt.tight_layout()
#plt.text(x,y,"Here")
plt.show()

print(np.unique(labeled_coins))