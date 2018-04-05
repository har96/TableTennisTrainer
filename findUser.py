from freenect import sync_get_depth as get_depth, sync_get_video as get_video
import cv2 
import numpy as np
import sys
from drawTable import drawTable
from frame_convert2 import video_cv, pretty_depth

if len(sys.argv) != 2:
    windows = ""
else: windows = sys.argv[1]

def get_contour(contours, min, max):
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        if w > min and w < max:
           return c

def get_contour2(contours, min, max):
    for c in contours:
        (x,y), radius = cv2.minEnclosingCircle(c)
        if radius > min and radius < max:
            return c

def prepare_depth(image):
    img = pretty_depth(image)
    img = cv2.medianBlur(img, 5)
    return img

def create_windows():
    if 'd' in windows:
        cv2.namedWindow('depth')
    if 'c' in windows:
        cv2.namedWindow('color')
    if 't' in windows:
        cv2.namedWindow('threshold')
    if 'g' in windows:
        cv2.namedWindow('grid')

  
def doloop():
    global depth, rgb

    
    create_windows()

    cv2.createTrackbar('distance min', 'color', 0, 255, lambda x: None)
    cv2.createTrackbar('distance max', 'color', 0, 255, lambda x: None)
    nothing = lambda x: None
    cv2.createTrackbar('min', 'color', 0, 500, nothing)
    cv2.createTrackbar('max', 'color', 0, 1000, nothing)
    
    distance_max = 249
    distance_min = 215
    min = 45
    max = 120
    while True:
        # Get a fresh frame
        (depth,_), (rgb,_) = get_depth(), get_video()
        
        # Get contours
        depth = prepare_depth(depth)
        ret, thresh1 = cv2.threshold(depth, distance_min, 255, cv2.THRESH_TOZERO)
        ret, thresh = cv2.threshold(thresh1, distance_max, 255, cv2.THRESH_TOZERO_INV)
        if 'd' in windows: cv2.imshow('depth', depth)
        if 't' in windows: cv2.imshow('threshold', thresh)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Get target point
        target = get_contour2(contours, min, max)
        if not target is None:
            M = cv2.moments(target)
            if M['m00'] == 0: print "0"
            else:
	        target_point = ( int(M['m10']/M['m00']), int(M['m01']/M['m00']) )

                x_val = (640.0 / float(target_point[0]) * 255)
                _, radius = cv2.minEnclosingCircle(target)
                #cv2.putText(rgb, str(radius), target_point, cv2.FONT_HERSHEY_SIMPLEX, \
                    #1, (0,255,0), 2, cv2.CV_AA)
                cv2.circle(rgb, target_point, 4, (255,0,0), -1)
                cv2.drawContours(rgb, [target], -1, (0, 255, 0), 3)

                if 'g' in windows: cv2.imshow('grid', drawTable(target_point[0]))


        if 'c' in windows: cv2.imshow('color', video_cv(rgb))
        char = cv2.waitKey(100)
        if char == 27:
            cv2.destroyAllWindows()
            break
        elif char == 115:
            cv2.imwrite('capture.png', video_cv(rgb))
            cv2.namedWindow('saved')
            cv2.imshow('saved', video_cv(rgb))

        #distance_min = cv2.getTrackbarPos('distance min', 'rgb')
        #distance_max = cv2.getTrackbarPos('distance max', 'rgb')
        #min = cv2.getTrackbarPos('min', 'rgb')
        #max = cv2.getTrackbarPos('max', 'rgb')
        
doloop()
