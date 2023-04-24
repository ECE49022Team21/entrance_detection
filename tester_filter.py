import cv2
import sys
import numpy as np
import time

a_1 = 30
a_2 = 20
a_3 = 1000

#def nothing(x):
#    pass
#cv2.namedWindow('image')

#cv2.createTrackbar('1','image',0,255,nothing)
#cv2.createTrackbar('2','image',0,255,nothing)
#cv2.createTrackbar('3','image',0,255,nothing)

img = cv2.imread('Cali_f_47.png')
#new_dim = (400,325)
#img = cv2.resize(img,new_dim)


    #a_1 = cv2.getTrackbarPos('1','image')
    #a_2 = cv2.getTrackbarPos('2','image')
    #a_3 = cv2.getTrackbarPos('3','image')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.bilateralFilter(img,30,50,50)
cv2.imwrite('New_image_1.png',img)
kernel = np.array([[0, -1, 0],
                   [-1, 4.9,-1],
                   [0, -1, 0]])
img = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)

    #cv2.resizeWindow('image',1000,600)
cv2.imwrite('New_image.png',img)




