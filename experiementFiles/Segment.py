from skimage.filters import sobel
from skimage.segmentation import watershed
from scipy import ndimage as ndi
import matplotlib.pyplot as plt
import numpy as np
import cv2

img = cv2.imread("TestData//Left.png",cv2.COLOR_BGR2GRAY)

markers = np.zeros_like(img)
markers[img < 30] = 2
markers[img > 150] = 1

elevation_map = sobel(img)
segmentation = watershed(elevation_map, markers)
segmentation = ndi.binary_fill_holes(segmentation - 1) # I believe this sets that background as 0 so we don't change it
labeled_img, num_features = ndi.label(segmentation)

print(num_features)
print(np.unique(labeled_img))

test = np.array([[0, 0, 0, 0, 0],
				 [0, 1, 1, 1, 0],
				 [0, 1, 1, 1, 0],
				 [2, 2, 2, 2, 2],
				 [0, 2, 2, 2, 2]])

test = labeled_img

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

ax = plt.figure(figsize=(9, 3))

plt.subplot(121)
plt.imshow(test)
plt.title("before")
test[y][x] == 255

plt.subplot(122)
plt.imshow(test)
plt.title("after")
plt.text(x,y,"Here")
plt.show()