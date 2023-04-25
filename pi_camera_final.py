#***** Camera *****#
from picamera.array import PiRGBArray #For Reading from the Camera (using PiRGBArray is suppose to help with processing time)
from picamera import PiCamera         #For Preprocessing Adjustments (exposure,gain,sharpness,etc.)
import time                           #For Time Date Stamp when Outputing Data
import cv2                            #For OpenCV Filters
import numpy as np                    #For Grabing Numpy Array of Raw Images & Array Manipulation in General Throughout Program
import keyboard                       #For Interupting Function
import argparse
import cv2


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
	arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
	# Initialize the detector parameters - picked a working combination from millions of random examples
	parameters =  cv2.aruco.DetectorParameters_create()
	parameters.minDistanceToBorder =  1 #d3
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
	frame_width = 640#640#1024#1088#640#1088#640
	frame_height = 480#480#720#480#720#480
	camera.resolution = (frame_width, frame_height)     
	camera.framerate = 120                              #Max 120 @ 640:480
	camera.sharpness = 70                               #-100:to:100
	camera.contrast = 0                                 #-100:to:100
	camera.brightness = 50                              #   0:to:100
	camera.saturation = 0                               #-100:to:100
	camera.exposure_compensation = 0                    # -25:to:25
	time.sleep(2)
	camera.exposure_mode = 'off'
	camera.awb_mode = 'off'                             #A lot of Auto Modes see get_picam_parameters.py
	gain_r = 2.5                                        #0:to:8
	gain_b = 2.1                                        #0:to:8
	camera.awb_gains = (gain_r, gain_b)
	camera.sensor_mode = 7                              #There are 7 different modes to be set for the sensor (7 is the lowest resolution with the highest frame rate possible for OV5647)
	camera.shutter_speed = 3600                         #(this parameter has a direct correlation to the frame rate and exposure speed) (units is microseconds)
	rawCapture = PiRGBArray(camera, size=(frame_width, frame_height))    #Array for Reading Camera Frames

	return frame_width,frame_height,camera,rawCapture,arucoDict,parameters

#***** Capute Frames *****#
def capture_frames(frame_width,frame_height,camera,rawCapture,arucoDict,arucoParams):
	#Grab the raw NumPy array representing the image (can also use 'yuv' instead of bgr)
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):          
																			
		image_norm = frame.array

		# detect ArUco markers in the input frame
		(corners, ids, rejected) = cv2.aruco.detectMarkers(image_norm,arucoDict, parameters=arucoParams)
				
		# verify *at least* one ArUco marker was detected
		if len(corners) > 0:
			rawCapture.truncate(0)
			return True
		else:
			rawCapture.truncate(0)
			return False
		#cv2.imshow("Raw Image", image_norm)

	camera.close()

if __name__ == "__main__":
	a,b,c,d,e,f = marker_cam_setup()
	capture_frames(a,b,c,d,e,f)
