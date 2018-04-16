from freenect import sync_get_depth as get_depth, sync_get_video as get_video
import cv2 
import numpy as np
import sys
from drawTable import drawTable
from strategy import *
from frame_convert2 import video_cv, pretty_depth
import serial
import time

DISTANCE_MAX = 249
DISTANCE_MIN = 215
MIN_A = 65
MAX_A = 120
EDGE = 20

WIDTH = 640
HEIGHT = 575

if len(sys.argv) < 2:
    print "USAGE: findUser.py windows serial_handle"
    windows = ""
else: 
    windows = sys.argv[1]
    if len(sys.argv) == 3:
        try:
            serial_out = serial.Serial(sys.argv[2], 9600)
        except IOError:
            print "Failed to open serial bus"
            sys.exit(0)
    else: serial_out = None

def get_contour(contours, min_a, max_a):
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        if w > min_a and w < max_a:
           return c

def get_contour2(contours, min_a, max_a):
    for c in contours:
        (x,y), radius = cv2.minEnclosingCircle(c)
        if radius > min_a and radius < max_a:
            return c

def prepare_depth(image):
    """
    Prettify and format depth stream.
    """
    img = pretty_depth(image)
    img = cv2.medianBlur(img, 5)
    return img

def create_windows():
    """
    Open cv2 windows.
    """
    if 'd' in windows:
        cv2.namedWindow('depth')
    if 'c' in windows:
        cv2.namedWindow('color')
    if 't' in windows:
        cv2.namedWindow('threshold')
    if 'g' in windows:
        cv2.namedWindow('grid')
        cv2.setMouseCallback('grid', select_grid)
        cv2.imshow('grid', drawTable(0))

def select_target(positions, difficulty=0):
    """
    Receives a list of selected targets
    and picks one to shoot at based on difficulty.
    Random picks the latest, while other difficulties
    seeks to remove outliers.
    """
    return positions[-1]

def send_target(target):
    """
    Send target over serial.
    """
    current_speed = cv2.getTrackbarPos('Top Motor', 'grid')
    speedTop = cv2.getTrackbarPos('Bottom Motor', 'grid')
    rotate = cv2.getTrackbarPos('rotation', 'grid')
    if target:
        target = get_coords(target)
        data = "{} {} {} {} {}".format(speedTop, current_speed, target[1], target[0], rotate)
        print "----------------"
        print target
        print data
        serial_out.write(data)
    print "----------------"


def select_grid(event, x, y, flags, param):
    """
    Mouse event handler
    """
    global current_target
    if event == cv2.EVENT_LBUTTONDOWN:
        gridpoint = get_nearest_grid((x,y),WIDTH, HEIGHT, 50)
        current_target = gridpoint
    elif event == cv2.EVENT_RBUTTONDOWN and serial_out:
        # Send data
        send_target(current_target)

def doloop():
    """
    Primary process loop.
    """
    global depth, rgb, current_target


    current_target = None
    positions = []
    
    create_windows()

    nothing = lambda x: None
   # cv2.createTrackbar('distance min', 'color', 0, 255, nothing)
   # cv2.createTrackbar('distance max', 'color', 0, 255, nothing)
    cv2.createTrackbar('min', 'color', MIN_A, 500, nothing)
    cv2.createTrackbar('max', 'color', MAX_A, 1000, nothing)
    cv2.createTrackbar('trim', 'color', 0, 200, nothing)
    #cv2.createTrackbar('user', 'grid', 0, 640, nothing)
    cv2.createTrackbar('difficulty', 'grid', 0, 4, nothing)
    cv2.createTrackbar('Top Motor', 'grid', 170, 1023, nothing)
    cv2.createTrackbar('Bottom Motor', 'grid', 150, 1023, nothing)
    cv2.createTrackbar('rotation', 'grid', 90, 180, nothing)

    times = []
    
    while True:
        time.sleep(1)
        start = time.time()

        # Trackbar updates
        distance_min = cv2.getTrackbarPos('distance min', 'color')
        distance_max = cv2.getTrackbarPos('distance max', 'color')
        min_a = cv2.getTrackbarPos('min', 'color')
        max_a = cv2.getTrackbarPos('max', 'color')
        trim = cv2.getTrackbarPos('trim', 'color')
        difficulty = cv2.getTrackbarPos('difficulty', 'grid')
        userpos = cv2.getTrackbarPos('user', 'grid')
        if distance_min == -1: distance_min = DISTANCE_MIN
        if distance_max == -1: distance_max = DISTANCE_MAX
        if min_a == -1: min_a = MIN_A
        if max_a == -1: max_a = MAX_A
        if trim == -1: trim = EDGE
   
        # Get a fresh frame
        (depth,_), (rgb,_) = get_depth(), get_video()
        depth = prepare_depth(depth)

        # Trim frame
        if trim: 
            depth = depth[:,trim:depth.shape[1] - trim]
            rgb = rgb[:,trim:rgb.shape[1] - trim]
        
        # Threshold
        ret, thresh1 = cv2.threshold(depth, distance_min, 255, cv2.THRESH_TOZERO)
        ret, thresh = cv2.threshold(thresh1, distance_max, 255, cv2.THRESH_TOZERO_INV)
        if 'd' in windows: cv2.imshow('depth', depth)
        if 't' in windows: cv2.imshow('threshold', thresh)

        # Get target point
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        target = get_contour2(contours, min_a, max_a)
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

                if userpos == -1: userpos = target_point[0]

        if difficulty: 
            current_target = pick_target(userpos, difficulty)
            current_speed = pick_speed(userpos, difficulty)

        # Keep a list of the detected positions
        positions.append(current_target)
        if len(positions) == 5:
            # select and send target
            send_target(select_target(positions, difficulty))
            positions = []


        if 'g' in windows: 
            cv2.imshow('grid', drawTable(userpos, current_target))


        if 'c' in windows: cv2.imshow('color', video_cv(rgb))
        char = cv2.waitKey(10)
        if char == 27:
            cv2.destroyAllWindows()
            break
        elif char == 115:
            cv2.imwrite('capture.png', video_cv(rgb))
            cv2.namedWindow('saved')
            cv2.imshow('saved', video_cv(rgb))
        elif char == ord('r'):
            if serial_out: 
                serial_out.close()
                serial_out.open()

        end = time.time()
        times.append(end - start)
#         print "Detected user at position: ", userpos
#         print "Last loop: ", times[-1]
#         if len(times) > 2:
#             print "Average: ", sum(times[2:])/(len(times)-2)

       
doloop()
if serial_out: serial_out.close()
