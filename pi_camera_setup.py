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
		"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
		"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
		"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
		"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
		"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
		"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
		"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
		"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
		"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
		"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
		"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
		"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
		"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
		"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
		"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
		"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
		"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
		"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
		"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
		"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
		"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
	}
	# verify that the supplied ArUCo tag exists and is supported by opencv
	# if ARUCO_DICT.get(args["type"], None) is None:
	# 	print("[INFO] ArUCo tag of '{}' is not supported".format(
	# 		args["type"]))
	# 	sys.exit(0)
	# load the ArUCo dictionary and grab the ArUCo parameters
	print("[INFO] detecting '{}' tags...".format(args["type"]))
	arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
	arucoParams = cv2.aruco.DetectorParameters_create()
	# initialize the video stream and allow the camera sensor to warm up
	#print("[INFO] starting video stream...")
	#time.sleep(2.0)

	#***** CAMERA PRE-PROCESSING Parameters (use get_picam_paramters.py for adjustment) *****#
	camera = PiCamera()                                 #Connect to PiCamera
	frame_width = 1024#640#1024#1088#640#1088#640                                   #1280 #1920 #2592 
	frame_height = 720#480#720#480#720#480                                  #720  #1080 #1944 
	camera.resolution = (frame_width, frame_height)     #Other Resolutions Above
	camera.framerate = 120                               #Max 90 @ 640:480
	camera.sharpness = 0                              #-100:to:100
	camera.contrast = 0                                #-100:to:100
	camera.brightness = 50                              #   0:to:100
	camera.saturation = 0                             #-100:to:100
	camera.exposure_compensation = 0                    #-100:to:100
	time.sleep(1)
	camera.exposure_mode = 'off'
	camera.awb_mode = 'off'                             #A lot of Auto Modes see get_picam_parameters.py
	gain_r = 2.5                                       #   0:to:8
	gain_b = 2.1                                        #   0:to:8
	camera.awb_gains = (gain_r, gain_b)
	camera.sensor_mode = 7                              #There are 7 different modes to be set for the sensor (7 is the lowest resolution with the highest frame rate possible for OV5647)
	#camera.shutter_speed = 4000                         #Found between 500-1800 to be best range for OV5647   (500 is lowest it will go and still pick up something from camera) (this parameter has a direct correlation to the frame rate and exposure speed) (units is microseconds)
	rawCapture = PiRGBArray(camera, size=(frame_width, frame_height))    #Array for Reading Camera Frames
	#time.sleep(1)                                      #Allow Camera to "Warmup"
	#h,  w = image_norm.shape[:2]                       #May be Useful for further implementation (syntac to get current height and width of image and set to variables)

	return frame_width,frame_height,camera,rawCapture,arucoDict,arucoParams

#***** Capute Frames *****#
def capture_frames(frame_width,frame_height,camera,rawCapture,arucoDict,arucoParams):

	size_frame = (frame_width,frame_height)                                                                           #For writing to video file
	file_name_vid = "/home/ssafar/Pictures/Test_5_" + str(time.time()) + ".avi"  #Output Video Format/Location (look into lossless compression)
	fourcc = cv2.VideoWriter_fourcc(*'MJPG')                                                                        #Tried *'X264' as well, MJPG seems the best with loss compression #set equal to -1 to see all Codecs
	final_result = cv2.VideoWriter(file_name_vid,fourcc,1,size_frame)

	#key = cv2.waitKey(1) & 0x00 
	#if key == ord("s"):
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
			ids = ids.flatten()
			# loop over the detected ArUCo corners
			for (markerCorner, markerID) in zip(corners, ids):
				# extract the marker corners (which are always returned
				# in top-left, top-right, bottom-right, and bottom-left
				# order)
				corners = markerCorner.reshape((4, 2))
				(topLeft, topRight, bottomRight, bottomLeft) = corners
				# convert each of the (x, y)-coordinate pairs to integers
							#topRight = (int(topRight[0]), int(topRight[1]))
							#bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
				bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
				topLeft = (int(topLeft[0]), int(topLeft[1]))
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
				# draw the ArUco marker ID on the frame
							#cv2.putText(image_norm, str(markerID),(topLeft[0], topLeft[1] - 15),cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 95, 31), 2)
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
