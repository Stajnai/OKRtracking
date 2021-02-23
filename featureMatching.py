import numpy as np
import cv2 
from matplotlib import pyplot as plt

def resize(img):
	height,width = img.shape

	scale_percent = 512 / width
	width = int(img.shape[1] * scale_percent) #python makes it a float, and it needs an int
	height = int(img.shape[0] * scale_percent)
	img = cv2.resize(img,(width,height),interpolation = cv2.INTER_AREA)

	return img

MATCH_COUNT = 10
img1 = cv2.imread('TestData\\Left.png',0)           # queryImage
img2 = cv2.imread('TestData\\Right.png',0) 		# trainImage

# I want to be able to use these, but with the warpPerspective these caused an issue (havent been able to try with warpAffine yet)
img1 = resize(img1)
img2 =  resize(img2)


'''
# For testing if the images were correctly loaded
cv2.imshow("im1",img1)
cv2.waitKey(0)
cv2.imshow("im2",img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
 


# Initiate ORB detector - between sift, surf, and orb, orb is known to be the most efficient.
orb = cv2.ORB_create()

# find the keypoints and descriptors with ORB
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

matches = bf.match(des1,des2)
matches = sorted(matches, key = lambda x: x.distance)

# Apply ratio test
good = []
good_nonlist = []  #draw matches takes a non list
for m in matches:
	if m.distance < 0.75:
		good.append([m])
		good_nonlist.append(m)


img3 = cv2.drawMatches(img1,kp1,img2,kp2,good_nonlist, None,flags = 2) # needs a non list unlike what good was (do i need "good" anymore?)
plt.imshow(img3)
plt.show()

# Initialize lists
list_kp1 = []
list_kp2 = []

# For each match...
for mat in matches:

    # Get the matching keypoints for each of the images
    img1_idx = mat.queryIdx
    img2_idx = mat.trainIdx

    # x - columns
    # y - rows
    # Get the coordinates
    (x1, y1) = kp1[img1_idx].pt
    (x2, y2) = kp2[img2_idx].pt

    # Append to each list
    list_kp1.append((x1, y1))
    list_kp2.append((x2, y2))


h,status = cv2.findHomography(np.float32(list_kp1),np.float32(list_kp2))
M = np.float32(h) #tried converting to proper noation for warpAffine, but its not good enough
rows,cols = img2.shape

print(M)

#img4 = cv2.warpAffine(img1,M, (cols,rows))
img4 =  cv2.warpPerspective(img1,h,(cols,rows))

# Display images
#cv2.imshow("Source Image", img1)
#cv2.imshow("Destination Image", img2)
#cv2.imshow("Warped Source Image", img4)
#img5 = cv2.subtract(img4,img2)*20
#cv2.imshow("subtract",img5)



cv2.waitKey(0)
cv2.destroyAllWindows()
