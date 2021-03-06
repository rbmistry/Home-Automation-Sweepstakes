# -*- coding: utf-8 -*-
#!/usr/bin/env python
import cv2, sys
import numpy as np
import os
import webbrowser
import mraa
import time
print (mraa.getVersion())

button = mraa.Gpio(29)
button.dir(mraa.DIR_IN)

f = os.popen("ls -lrt /dev/video*") 
for line in f.readlines(): 
    print line
    camNO = int(line[-2])
    print "Camera detected:"

print camNO

url = 'http://localhost/Register'
def OpenUrl():
    
    #os.system("killall -KILL chromium")
    webbrowser.open(url,new=0)
    #pyautogui.hotkey('ctrl', 'w')  # ctrl-w to close the tab
    #keypress('keydown Control_L')
    #keypress('key w')
    #keypress('keyup Control_L')

def savepic():
    IMAGE_FILE = "/var/www/html/Register/pic.jpg"
    cv2.imwrite(IMAGE_FILE, frame)


# Constants
DEVICE_NUMBER = camNO
FONT_FACES = [
    cv2.FONT_HERSHEY_SIMPLEX,
    cv2.FONT_HERSHEY_PLAIN,
    cv2.FONT_HERSHEY_DUPLEX,
    cv2.FONT_HERSHEY_COMPLEX,
    cv2.FONT_HERSHEY_TRIPLEX,
    cv2.FONT_HERSHEY_COMPLEX_SMALL,
    cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
    cv2.FONT_HERSHEY_SCRIPT_COMPLEX
]
if len(sys.argv) > 1:
    XML_PATH = sys.argv[1]
else:
    print "Error: XML path not defined"
    sys.exit(1)

# Init the Cascade Classifier
# http://docs.opencv.org/modules/objdetect/doc/cascade_classification.html#cascadeclassifier
faceCascade = cv2.CascadeClassifier(XML_PATH)
#eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Init webcam
# http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-videocapture
vc = cv2.VideoCapture(DEVICE_NUMBER)

# Check if the webcam init was successful
# http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-isopened
if vc.isOpened(): # try to get the first frame
    # http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-read
    retval, frame = vc.read()
else:
    sys.exit(1)

# If webcam read successful, loop indefinitely
i = 0
buttoncount = 0
while retval:
    # Define the frame which the webcam will show
    e1 = cv2.getTickCount()
    touchButton = int(button.read())
    if(touchButton == 1):
        buttoncount=0
        #print "........................................",buttoncount, touchButton
    else:
        buttoncount = buttoncount+1
        #print "........................................",buttoncount, touchButton
        if (buttoncount == 15):
            savepic()
            OpenUrl()
            print "...............Button pressed..............."
                
    frame_show = frame
    if i%29 == 0:
        # Convert frame to grayscale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect objects and return an array of faces
            # http://docs.opencv.org/2.4/modules/objdetect/doc/cascade_classification.html#cascadeclassifier-detectmultiscale
        faces = faceCascade.detectMultiScale(
            frame,
            scaleFactor=1.2,
            minNeighbors=2,
            minSize=(50, 50),
            #flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        # http://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html#rectangle
        cv2.rectangle(frame_show, (x, y), (x+w, y+h), (0, 0, 255), 2)
        font_typeface = FONT_FACES[2]
        font_scale = .8
        font_color = (0,0,255)
        font_weight = 2
        x = 2
        y = 50
        cv2.putText(frame_show, "Press the RED button to enter for a Chance to Win:", (x,y), font_typeface, font_scale, font_color, font_weight)
        x = 2
        y = 70
        cv2.putText(frame_show, "One DragonBoard 410c", (x,y), font_typeface, font_scale, font_color, font_weight)

    # Show the image on the screen
    # http://docs.opencv.org/2.4/modules/highgui/doc/user_interface.html#imshow
    cv2.imshow('Facial Detection', frame_show)
    e2 = cv2.getTickCount()
    time = (e2 - e1)/ cv2.getTickFrequency()
    #print i, time
    #cv2.namedWindow('Facial Detection',cv2.WINDOW_AUTOSIZE)
    #cv2.resizeWindow('Facial Detection', 700,500)

    # Grab next frame from webcam
    retval, frame = vc.read()
	# Launch the Borwser if the spacebar is pressed
    # http://docs.opencv.org/2.4/modules/highgui/doc/user_interface.html#waitkey
    if cv2.waitKey(1) == 32:
    	#url = 'http://www.google.com'
    	#webbrowser.open_new(url)
        savepic()
        OpenUrl()
    # Exit program after waiting for a pressed key
    # http://docs.opencv.org/2.4/modules/highgui/doc/user_interface.html#waitkey
    if cv2.waitKey(1) == 27:
    	break
    # Launch the Borwser if the spacebar is pressed    


    i += 1



