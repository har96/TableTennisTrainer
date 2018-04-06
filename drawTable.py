import cv2
import numpy as np

def createBlank(width, height):
    img = np.zeros((height, width, 3), np.uint8)
    img[:,:] = (100, 150, 50)
    return img

def drawGrid(img, width, height):
    color = (0, 0, 0)
    for i in range(13):
       offset = 20 + i*50
       cv2.line(img, (offset, 0), (offset, height), color, 1)
       if i < 10:
           cv2.line(img, (0, offset), (width, offset), color, 1)


    return img

def drawTable(userPos, current_target=None):
    width = 640
    height = 575  # 640/ (1.525/(2.74*0.5))
    img = createBlank(width, height)

    #Draw user
    cv2.circle(img, (userPos, 0), 20, (200,0,0), -1)
    
    # net
    #cv2.putText(img, "NET", (290, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,50), 2, cv2.CV_AA)

    # Half mark
    cv2.rectangle(img, (width/2 - 1,25), (width/2 + 1, height - 25), (255,255,255), 2)

    if current_target:
        cv2.rectangle(img, (current_target[0]-25, current_target[1]-25), \
                (current_target[0] + 25, current_target[1] + 25), (10, 10, 255), 2)

    return drawGrid(img, width, height)


def main():
    cv2.namedWindow('table')

    #display
    cv2.imshow('table', drawTable(250))


    cv2.waitKey()
    cv2.destroyAllWindows()
    return

if __name__ == '__main__':
    main()
