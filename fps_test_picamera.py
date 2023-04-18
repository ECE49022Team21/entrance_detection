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
	print("[INFO] detecting '{}' tags...".format(args["type"]))
	arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
	arucoParams = cv2.aruco.DetectorParameters_create()

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
	
	return frame_width,frame_height,camera,rawCapture,arucoDict,arucoParams

# Initialize variables for FPS calculation
start_time = time.time()
frame_count = 0
#***** Capute Frames *****#
def capture_frames(frame_width,frame_height,camera,rawCapture,arucoDict,arucoParams):
  
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):          #Grab the raw NumPy array representing the image (can also use 'yuv' instead of bgr)
																			#Need this line for sudo command to run with Video
		image_norm = frame.array
		(corners, ids, rejected) = cv2.aruco.detectMarkers(image_norm,arucoDict, parameters=arucoParams)
				# verify *at least* one ArUco marker was detected
		if len(corners) > 0:
			# flatten the ArUco IDs list
			ids = ids.flatten()
			# loop over the detected ArUCo corners
			for (markerCorner, markerID) in zip(corners, ids):
				corners = markerCorner.reshape((4, 2))
				(topLeft, topRight, bottomRight, bottomLeft) = corners
				cX = int((topLeft[0] + bottomRight[0]) / 2.0)
				cY = int((topLeft[1] + bottomRight[1]) / 2.0)
				cv2.circle(image_norm, (cX, cY), 5, (0, 40, 200), -1)
		cv2.imshow("Raw Image", image_norm)
    rawCapture.truncate(0)
        # calculate elapsed time
    elapsed_time = time.time() - start_time
    frame_count += 1
    
        # update FPS every second
    if elapsed_time >= 1:
        fps = frame_count / elapsed_time
        print(f'FPS: {fps:.2f}')
        start_time = time.time()
        frame_count = 0
    
		key = cv2.waitKey(1) & 0xF
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break
			#clear frame from buffer
		#rawCapture.truncate(0)
	camera.close()

	return 0

if __name__ == "__main__":
	a,b,c,d,e,f = marker_cam_setup()
	capture_frames(a,b,c,d,e,f)
