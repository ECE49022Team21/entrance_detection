import numpy as np
import cv2 as cv
import glob
import time



################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################

chessboardSize = (4,3)# (13,9)
#frameSize = (2028,1080)
frameSize = (3200,1800)


# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 200, 0.01)


# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

size_of_chessboard_squares_mm = 170
objp = objp * size_of_chessboard_squares_mm


# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

found = 0
images = glob.glob('*.png')
ct = 0
for image in images:
    ct += 1
    img = cv.imread(image)
    #img = img.resize(1600,900)
    
    #new_dim = (800,450)
    new_dim = (1600,900)
    #img = cv.resize(img,new_dim)
    #img = cv.bilateralFilter(img,30,50,50)
    #kernel = np.array([[0, -1, 0],
    #               [-1, 5,-1],
    #               [0, -1, 0]])
    #img = cv.filter2D(src=img, ddepth=-1, kernel=kernel)
    #blur = cv.bilateralFilter(img,9,75,75)
    #cv.imshow("blur",blur)
    #time.sleep(5)
    #grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #cv.imshow('grey',grey)
    #cv.waitKey(1000)
    ## Color-segmentation to get binary mask
    ##lwr = np.array([0, 0, 143])
    ##upr = np.array([179, 61, 252])
    #lwr = np.array([0,0,150])
    #upr = np.array([115,60,250])
    #hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    #msk = cv.inRange(hsv, lwr, upr)

    ## Extract chess-board
    #krn = cv.getStructuringElement(cv.MORPH_RECT, (50, 30))
    #dlt = cv.dilate(msk, krn, iterations=5)
    #res = 255 - cv.bitwise_and(dlt, msk)

    ## Displaying chess-board features
    #res = np.uint8(res)
    #cv.imshow('res',res)
    #cv.waitKey(5000)
    
    
    # Find the chess board corners
    print("Searching")
    ret, corners = cv.findChessboardCorners(img, chessboardSize, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FILTER_QUADS)
    print("Complete")
    print("Count: ",ct)
    #ret, corners = cv.findCirclesGrid(gray, chessboardSize, None)
    #found = 0
    # If found, add object points, image points (after refining them)
    if ret == True:
        found += 1
        print("Found",found)
        objpoints.append(objp)
        #corners2 = cv.cornerSubPix(img, corners, (2,2), (-1,-1), criteria)
        imgpoints.append(corners)

        # Draw and display the corners
        cv.drawChessboardCorners(img, chessboardSize, corners, ret)
        cv.imshow('img', img)
        cv.waitKey(1000)

print('Total Found: ', found)
cv.destroyAllWindows()




############## CALIBRATION #######################################################

ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize, None, None)
print("Camera Calibrated: ", ret)
print("\nCamera Matrix:\n", cameraMatrix)
print("\nDistortion Parameters:\n", dist)
print("\nRotation Vectors\n", rvecs)
print("\nTranslation Vectors:\n", tvecs)

############## UNDISTORTION #####################################################

#img = cv.imread('img_s_7.png')
#h,  w = img.shape[:2]
#newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))



# # Undistort
#dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

# # crop the image
#x, y, w, h = roi
#dst = dst[y:y+h, x:x+w]
#dim=[]
#dim = dim[640, 480]
#cv.imwrite('result.png',dst)



# # Undistort with Remapping
# mapx, mapy = cv.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
# dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

# # crop the image
# x, y, w, h = roi
# dst = dst[y:y+h, x:x+w]
# cv.imwrite('caliResult2.png', dst)




# # Reprojection Error
# mean_error = 0

# for i in range(len(objpoints)):
#     imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
#     error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
#     mean_error += error

# print( "total error: {}".format(mean_error/len(objpoints)) )
