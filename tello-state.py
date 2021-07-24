import cv2
import numpy as np
from datetime import datetime
from djitellopy import Tello

framewidth = 768
frameheight = 480
framerate = 30
maxArea = 0
count = 0
path = 'Z:/Data Science/Data/a4pic1.jpg'

#cap = cv2.VideoCapture(0)
#cap.set(3,framewidth)
#cap.set(4,frameheight)
#cap.set(10,150)
me = Tello()
me.connect()
#me.takeoff()
me.streamoff()
me.streamon()
#me.set_speed(50)

#me.move_forward(30)

def contour(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        return area

while True:
    if count%100 ==0:
        frame_read = me.get_frame_read()
        #ret, myframe = cap.read()
        myframe = frame_read.frame
        img = cv2.resize(myframe, (framewidth, frameheight))
        overlay = img.copy()
        output = img.copy()

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.date()
        battery = str(me.get_battery())
        #battery = 'No battery'


        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img_canny = cv2.Canny(img_gray,100,100)
        kernel = np.ones((5, 5))
        imgdil = cv2.dilate(img_canny, kernel, iterations=2)
        imgthreshold = cv2.erode(imgdil, kernel, iterations=1)

        contours, hierarchy = cv2.findContours(imgthreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        max_area = areas[max_index]
        cnt = contours[max_index]
        cv2.drawContours(output,cnt,-1,(255,0,0),2)

        cv2.rectangle(overlay, (304, 190), (464, 290), (0, 0, 255), 2)
        cv2.circle(overlay, (384, 240), 2, (0, 0, 255), -1)
        cv2.line(overlay, (384, 225), (384, 235), (100, 0, 255), 2)
        cv2.line(overlay, (384, 245), (384, 255), (100, 0, 255), 2)
        cv2.line(overlay, (369, 240), (379, 240), (100, 0, 255), 2)
        cv2.line(overlay, (389, 240), (399, 240), (100, 0, 255), 2)
        cv2.putText(overlay, "Time = {}".format(current_time), (10, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
        cv2.putText(overlay, "Date = {}".format(current_date), (10, 40), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
        cv2.putText(overlay, "Battery = {}".format(battery), (10, 455), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255), 1)
        cv2.putText(overlay, "Contour Area = {}".format(max_area), (10, 470), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255), 1)
        if max_area>180000:
            cv2.putText(overlay, "Prepare for impact", (50, 240), cv2.FONT_HERSHEY_TRIPLEX, 2,
                        (0, 0, 255), 1)



        cv2.addWeighted(overlay, 0.75, output, 0.5, 0, output)

        cv2.imshow('l', imgthreshold)
        cv2.imshow('Drone Stream',output)
        #while areas<20000:
        #me.move_forward(30)
    count += 1

    if cv2.waitKey(1) & 0xFF ==ord('q'):
        #me.land()
        break
    count += 1
cv2.destroyAllWindows()