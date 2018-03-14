from freenect import sync_get_depth as get_depth, sync_get_video as get_video
import cv2 
import numpy as np
from frame_convert2 import video_cv, pretty_depth

def get_contour(contours, min, max):
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        if w > min and w < max:
           return c
  
def doloop():
    global depth, rgb

    cv2.namedWindow('depth')
    cv2.namedWindow('rgb')

    #cv2.createTrackbar('threshold', 'rgb', 0, 255, lambda x: None)
    nothing = lambda x: None
    #cv2.createTrackbar('min', 'rgb', 0, 500, nothing)
    #cv2.createTrackbar('max', 'rgb', 0, 1000, nothing)
    
    threshold = 230
    min = 100
    max = 500
    while True:
        # Get a fresh frame
        (depth,_), (rgb,_) = get_depth(), get_video()
        
        # Get contours
        depth = pretty_depth(depth)
        ret, thresh = cv2.threshold(depth, threshold, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Get target point
        target = get_contour(contours, min, max)
        if not target is None:
            M = cv2.moments(target)
            target_point = ( int(M['m10']/M['m00']), int(M['m01']/M['m00']) )
            cv2.circle(rgb, target_point, 4, (255,0,0), -1)
            cv2.drawContours(rgb, [target], -1, (0, 255, 0), 3)

        cv2.imshow('depth', depth)
        cv2.imshow('rgb', video_cv(rgb))
        if cv2.waitKey(100) == 27:
            cv2.destroyAllWindows()
            break

        #threshold = cv2.getTrackbarPos('threshold', 'rgb')
        #print threshold
        #min = cv2.getTrackbarPos('min', 'rgb')
        #max = cv2.getTrackbarPos('max', 'rgb')
        
doloop()
