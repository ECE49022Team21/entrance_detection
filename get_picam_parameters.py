#Adopted from http://helloraspberrypi.blogspot.com/2015/12/python-to-capture-image-from-pi-camera_17.html by Erik
import picamera
import tkinter as tk
from tkinter import ttk
import time
from PIL import ImageTk, Image
from threading import Thread
import io
import sys
from pkg_resources import require

RQS_0=0
RQS_QUIT=1
RQS_CAPTURE=2
rqs=RQS_0
rqsUpdateSetting=True

def camHandler():
    global rqs
    rqs = RQS_0
    
    camera = picamera.PiCamera()
    #stream = io.BytesIO()

    #set default
    camera.sharpness = 0
    camera.contrast = 0
    camera.brightness = 50
    camera.saturation = 0
    camera.ISO = 0
    camera.video_stabilization = False
    camera.exposure_compensation = 0
    camera.exposure_mode = 'auto'
    camera.meter_mode = 'average'
    camera.awb_mode = 'auto'
    camera.image_effect = 'none'
    camera.color_effects = None
    #camera.rotation = 0
    camera.rotation = 270
    camera.hflip = False
    camera.vflip = False
    camera.crop = (0.0, 0.0, 1.0, 1.0)
    #camera.resolution = (1024, 768)
    #camera.resolution = (2592, 1944)
    #camera.resolution = (400,300)
    #camera.resolution = (720,480)
    camera.resolution = (1080,720)
    #time.sleep(1)
    #end of set default
    #camera.start_preview()

    while rqs != RQS_QUIT:
        #check if need update setting
        global rqsUpdateSetting
        if rqsUpdateSetting == True:
            rqsUpdateSetting = False
            camera.sharpness = scaleSharpness.get()
            camera.contrast = scaleContrast.get()
            camera.brightness = scaleBrightness.get()
            camera.saturation = scaleSaturation.get()
            camera.exposure_compensation = scaleExpCompensation.get()

            awb_mode_setting = varAwbMode.get()
            labelAwbVar.set(awb_mode_setting)
            camera.awb_mode = awb_mode_setting

            if awb_mode_setting == "off":
                gr = scaleGainRed.get()
                gb = scaleGainBlue.get()
                gAwb = (gr, gb)
                camera.awb_gains = gAwb
                labelAwbVar.set(awb_mode_setting + " : "
                    + str(gAwb))
        
        if rqs == RQS_CAPTURE:
            print("Capture")
            rqs=RQS_0
            timeStamp = time.strftime("%Y%m%d-%H%M%S")
            jpgFile='img_'+timeStamp+'.jpg'
            camera.resolution = (2592, 1944)    #set photo size
            camera.capture(jpgFile)
            camera.resolution = (400, 300)      #resume preview size
            labelCapVal.set(jpgFile)
        else:
            stream = io.BytesIO()
            camera.capture(stream, format='jpeg')
            stream.seek(0)
            tmpImage = Image.open(stream)
            tmpImg = ImageTk.PhotoImage(tmpImage)
            previewPanel.configure(image = tmpImg)
            #sleep(0.5)
                
    print("Quit")        
    #camera.stop_preview()
    
def startCamHandler():
    camThread = Thread(target=camHandler)
    camThread.start()

def quit():
    global rqs
    rqs=RQS_QUIT

    global tkTop
    tkTop.destroy()

def capture():
    global rqs
    rqs = RQS_CAPTURE
    labelCapVal.set("capturing")

def cbScaleSetting(new_value):
    global rqsUpdateSetting
    rqsUpdateSetting = True

def cbButtons():
    global rqsUpdateSetting
    rqsUpdateSetting = True

tkTop = tk.Tk()
tkTop.wm_title("Raspberry Pi Camera")
tkTop.geometry('800x500')

previewWin = tk.Toplevel(tkTop)
previewWin.title('Preview')
previewWin.geometry('400x300')
previewPanel = tk.Label(previewWin)
previewPanel.pack(side = "bottom", fill = "both", expand = "yes")

tk.Label(tkTop, text="http://helloraspberrypi.blogspot.com/").pack()
tk.Label(tkTop, text=require('picamera')).pack()

tkButtonQuit = tk.Button(
    tkTop, text="Quit", command=quit)
tkButtonQuit.pack()

tkButtonCapture = tk.Button(
    tkTop, text="Capture", command=capture)
tkButtonCapture.pack()

SCALE_WIDTH = 780;

labelCapVal = tk.StringVar()
tk.Label(tkTop, textvariable=labelCapVal).pack()

notebook = ttk.Notebook(tkTop)
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
notebook.add(frame1, text='Setting')
notebook.add(frame2, text='White Balance')
notebook.pack()

# Tab Setting
scaleSharpness = tk.Scale(
    frame1,
    from_=-100, to=100,
    length=SCALE_WIDTH,
    orient=tk.HORIZONTAL,
    label="sharpness",
    command=cbScaleSetting)
scaleSharpness.set(0)
scaleSharpness.pack(anchor=tk.CENTER)

scaleContrast = tk.Scale(
    frame1,
    from_=-100, to=100,
    length=SCALE_WIDTH,
    orient=tk.HORIZONTAL,
    label="contrast",
    command=cbScaleSetting)
scaleContrast.set(0)
scaleContrast.pack(anchor=tk.CENTER)

scaleBrightness = tk.Scale(
    frame1,
    from_=0, to=100,
    length=SCALE_WIDTH,
    orient=tk.HORIZONTAL,
    label="brightness",
    command=cbScaleSetting)
scaleBrightness.set(50)
scaleBrightness.pack(anchor=tk.CENTER)

scaleSaturation = tk.Scale(
    frame1,
    from_=-100, to=100,
    length=SCALE_WIDTH,
    orient=tk.HORIZONTAL,
    label="saturation",
    command=cbScaleSetting)
scaleSaturation.set(0)
scaleSaturation.pack(anchor=tk.CENTER)

scaleExpCompensation = tk.Scale(
    frame1,
    from_=-25, to=25,
    length=SCALE_WIDTH,
    orient=tk.HORIZONTAL,
    label="exposure_compensation",
    command=cbScaleSetting)
scaleExpCompensation.set(0)
scaleExpCompensation.pack(anchor=tk.CENTER)

# Tab White Balance

lfAwbMode = ttk.LabelFrame(frame2, text="awb_mode")
lfAwbMode.pack(fill="x", expand="yes")
lfAwbGains = ttk.LabelFrame(frame2, text="awb_gains")
lfAwbGains.pack(fill="x", expand="yes")

labelAwbVar = tk.StringVar()
tk.Label(lfAwbMode, textvariable=labelAwbVar).pack()

#--
AWB_MODES = [
    ("off", "off"),
    ("auto", "auto"),
    ("sunlight", "sunlight"),
    ("cloudy", "cloudy"),
    ("shade", "shade"),
    ("tungsten", "tungsten"),
    ("fluorescent", "fluorescent"),
    ("incandescent", "incandescent"),
    ("flash", "flash"),
    ("horizon", "horizon"),
    ]

varAwbMode = tk.StringVar()
varAwbMode.set("auto")
for text, awbmode in AWB_MODES:
    awbModeBtns = tk.Radiobutton(
        lfAwbMode,
        text=text,
        variable=varAwbMode,
        value=awbmode,
        command=cbButtons)
    awbModeBtns.pack(anchor=tk.W)
#--
scaleGainRed = tk.Scale(
    lfAwbGains,
    from_=0.0, to=8.0,
    resolution=0.1,
    length=SCALE_WIDTH,
    orient=tk.HORIZONTAL,
    label="Red",
    command=cbScaleSetting)
scaleGainRed.set(0.0)
scaleGainRed.pack(anchor=tk.CENTER)

scaleGainBlue = tk.Scale(
    lfAwbGains,
    from_=0.0, to=8.0,
    resolution=0.1,
    length=SCALE_WIDTH,
    orient=tk.HORIZONTAL,
    label="Blue",
    command=cbScaleSetting)
scaleGainBlue.set(0.0)
scaleGainBlue.pack(anchor=tk.CENTER)
#
print("start")
startCamHandler()

tk.mainloop()

