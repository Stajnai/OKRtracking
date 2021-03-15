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

plt.imshow(markers,cmap = 'gray')
plt.title("Markers")
plt.show()



ax = plt.figure(figsize=(9, 9))

plt.subplot(231)
plt.imshow(markers,cmap = 'gray')
plt.title("Markers")

elevation_map = sobel(coins)

plt.subplot(232)
plt.imshow(elevation_map)
plt.title("Elevation Map")

segmentation = watershed(elevation_map, markers)

plt.subplot(233)
plt.imshow(segmentation)
plt.title("Seg 1")

segmentation = ndi.binary_fill_holes(segmentation - 1) # I believe this sets that background as 0 so we don't change it

plt.subplot(234)
plt.imshow(segmentation)
plt.title("Seg 2 fill holes")

labeled_coins, num_features = ndi.label(segmentation)

print(num_features)

plt.subplot(235)
plt.imshow(labeled_coins)
plt.title("Labeled Coins")

plt.show()

print(np.unique(labeled_coins))

'''
from skimage import measure
all_labels = measure.label(coins)
labels = measure.label(coins, background=1)
plt.imshow(labels)
plt.show()

#print(labels)
'''
