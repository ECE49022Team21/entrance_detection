#***** Camera *****#
from picamera.array import PiRGBArray #For Reading from the Camera (using PiRGBArray is suppose to help with processing time)
from picamera import PiCamera         #For Preprocessing Adjustments (exposure,gain,sharpness,etc.)
import time                           #For Time Date Stamp when Outputing Data
import cv2                            #For OpenCV Filters
import numpy as np                    #For Grabing Numpy Array of Raw Images & Array Manipulation in General Throughout Program
#from skimage import exposure          #For Gamma Filter
#import keyboard                       #For Interupting Animate Function to Initialize Tare/Actuation

#***** CAMERA PRE-PROCESSING Parameters (use get_picam_paramters.py for adjustment) *****#
camera = PiCamera()                                 #Connect to PiCamera
frame_width = 640#1088#640                                   #1280 #1920 #2592 
frame_height = 480#720#480                                  #720  #1080 #1944 
camera.resolution = (frame_width, frame_height)     #Other Resolutions Above
camera.framerate = 90                               #Max 90 @ 640:480
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
#camera.shutter_speed = 1200                         #(500 is lowest it will go and still pick up something from camera) (this parameter has a direct correlation to the frame rate and exposure speed) (units is microseconds)
rawCapture = PiRGBArray(camera, size=(frame_width, frame_height))    #Array for Reading Camera Frames
time.sleep(1)                                      #Allow Camera to "Warmup"
#h,  w = image_norm.shape[:2]                       #May be Useful for further implementation (syntac to get current height and width of image and set to variables)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):          #Grab the raw NumPy array representing the image (can also use 'yuv' instead of bgr)
        key = cv2.waitKey(1) & 0xFF                                                                 #Need this line for sudo command to run with Video
        image_norm = frame.array
        cv2.imshow("Raw Image", image_norm)
        rawCapture.truncate(0)
