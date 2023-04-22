#***** Camera *****#
from picamera.array import PiRGBArray #For Reading from the Camera (using PiRGBArray is suppose to help with processing time)
from picamera import PiCamera         #For Preprocessing Adjustments (exposure,gain,sharpness,etc.)
import time                           #For Time Date Stamp when Outputing Data
import cv2                            #For OpenCV Filters
import numpy as np                    #For Grabing Numpy Array of Raw Images & Array Manipulation in General Throughout Program
#from skimage import exposure          #For Gamma Filter
import keyboard                       #For Interupting Function

import argparse
import imutils
import cv2
import sys

#***** ARUCO MARKER SETUP *****#
def marker_cam_setup():

	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-t", "--type", type=str,
		default="DICT_APRILTAG_16h5",
		help="type of ArUCo tag to detect")
	args = vars(ap.parse_args())
	# define names of each possible ArUco tag OpenCV supports
	ARUCO_DICT = {
		"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	}

	# load the ArUCo dictionary and grab the ArUCo parameters
	print("[INFO] Setting up to detect '{}' tags...".format(args["type"]))
	arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])

	# Initialize the detector parameters - picked a working combination from millions of random examples
	parameters =  cv2.aruco.DetectorParameters_create()
	parameters.minDistanceToBorder =  1
	#parameters.cornerRefinementMaxIterations = 10
	parameters.minOtsuStdDev= 1.5 #d3
	parameters.adaptiveThreshWinSizeMin= 3 #d3
	parameters.adaptiveThreshWinSizeStep= 9 #kills frames lower d10
	parameters.minMarkerDistanceRate= .05 #d.05 
	parameters.maxMarkerPerimeterRate= 3.5 #d4 kills frames
	parameters.minMarkerPerimeterRate= .025 #kills frames d3q
	parameters.polygonalApproxAccuracyRate= .035 #.d03 kills frames
	parameters.cornerRefinementWinSize= 5 #d5
	parameters.adaptiveThreshConstant= 8
	parameters.adaptiveThreshWinSizeMax= 23
	parameters.minCornerDistanceRate= .05

	#***** CAMERA PRE-PROCESSING Parameters (use get_picam_paramters.py for adjustment) *****#
	camera = PiCamera()                                 #Connect to PiCamera
	frame_width = 640#640#1024#1088#640#1088#640                                   #1280 #1920 #2592 
	frame_height = 480#480#720#480#720#480                                  #720  #1080 #1944 
	camera.resolution = (frame_width, frame_height)     #Other Resolutions Above
	camera.framerate = 120                               #Max 90 @ 640:480
	camera.sharpness = 100                              #-100:to:100
	camera.contrast = 0                                #-100:to:100
	camera.brightness = 50                              #   0:to:100
	camera.saturation = 0                             #-100:to:100
	camera.exposure_compensation = 0                    #-25:to:25
	time.sleep(2)
	print('Exposure Set')
	camera.exposure_mode = 'off'
	camera.awb_mode = 'off'                             #A lot of Auto Modes see get_picam_parameters.py
	gain_r = 2.5                                       #   0:to:8
	gain_b = 2.1                                        #   0:to:8
	camera.awb_gains = (gain_r, gain_b)
	camera.sensor_mode = 7                              #There are 7 different modes to be set for the sensor (7 is the lowest resolution with the highest frame rate possible for OV5647)
	camera.shutter_speed = 3600                         #Found between 500-1800 to be best range for OV5647   (500 is lowest it will go and still pick up something from camera) (this parameter has a direct correlation to the frame rate and exposure speed) (units is microseconds)
	rawCapture = PiRGBArray(camera, size=(frame_width, frame_height))    #Array for Reading Camera Frames

	return frame_width,frame_height,camera,rawCapture,arucoDict,parameters

#***** Capute Frames *****#
def capture_frames(frame_width,frame_height,camera,rawCapture,arucoDict,arucoParams):

	size_frame = (frame_width,frame_height)                                                                           #For writing to video file
	file_name_vid = "/home/ssafar/Pictures/Test_finals_" + str(time.time()) + ".avi"  #Output Video Format/Location (look into lossless compression)
	fourcc = cv2.VideoWriter_fourcc(*'MJPG')                                                                        #Tried *'X264' as well, MJPG seems the best with loss compression #set equal to -1 to see all Codecs
	final_result = cv2.VideoWriter(file_name_vid,fourcc,1,size_frame)

	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):          #Grab the raw NumPy array representing the image (can also use 'yuv' instead of bgr)
																			#Need this line for sudo command to run with Video
		image_norm = frame.array
		#image_norm = cv2.cvtColor(image_norm, cv2.COLOR_BGR2GRAY)
		# grab the frame from the threaded video stream and resize it
		# to have a maximum width of 1000 pixels
		#image_norm = imutils.resize(image_norm, width=600)
		# detect ArUco markers in the input frame
		(corners, ids, rejected) = cv2.aruco.detectMarkers(image_norm,arucoDict, parameters=arucoParams)
				
		# verify *at least* one ArUco marker was detected
		if len(corners) > 0:
			#qqprint("Detected Marker")
			# flatten the ArUco IDs list
			# ids = ids.flatten()
			# loop over the detected ArUCo corners
			for (markerCorner, markerID) in zip(corners, ids):
				#extract the marker corners (which are always returned
				# in top-left, top-right, bottom-right, and bottom-left
				# order)
				corners = markerCorner.reshape((4, 2))
				(topLeft, topRight, bottomRight, bottomLeft) = corners
				# convert each of the (x, y)-coordinate pairs to integers
							#topRight = (int(topRight[0]), int(topRight[1]))
							#bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
				#bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
				#topLeft = (int(topLeft[0]), int(topLeft[1]))
				# draw the bounding box of the ArUCo detection
							#cv2.line(image_norm, topLeft, topRight, (0, 255, 0), 2)
							#cv2.line(image_norm, topRight, bottomRight, (0, 255, 0), 2)
							#cv2.line(image_norm, bottomRight, bottomLeft, (0, 255, 0), 2)
							#cv2.line(image_norm, bottomLeft, topLeft, (0, 255, 0), 2)
				# compute and draw the center (x, y)-coordinates of the
				# ArUco marker
				cX = int((topLeft[0] + bottomRight[0]) / 2.0)
				cY = int((topLeft[1] + bottomRight[1]) / 2.0)
				cv2.circle(image_norm, (cX, cY), 5, (0, 40, 200), -1)
				#draw the ArUco marker ID on the frame
			    #cv2.putText(image_norm, str(markerID),(topLeft[0], topLeft[1] - 15),cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 95, 31), 2)
		# else:
		# 	rawCapture.truncate(0)
		# 	return False
		cv2.imshow("Raw Image", image_norm)
		#final_result.write(image_norm)
		key = cv2.waitKey(1) & 0xFF
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break
			#clear frame from buffer
		rawCapture.truncate(0)
	#cv2.detroyAllWindows()
	camera.close()

	return 0

if __name__ == "__main__":
	a,b,c,d,e,f = marker_cam_setup()
	capture_frames(a,b,c,d,e,f)
