import numpy as np
import random
import cv2
import math

#difficulties
EASY = 1
MEDIUM = 2
HARD = 3
RAND = 4

WIDTH = 640
HEIGHT = 575

def get_nearest_grid(point, width=WIDTH, height=HEIGHT, spacing=50):
    xs = np.arange(20,width, spacing)
    ys = np.arange(20, height, spacing)[:-2]
    x_i = (np.abs(xs - point[0])).argmin()
    y_i = (np.abs(ys - point[1])).argmin()

    return xs[x_i], ys[y_i]

def pick_target(userpos, difficulty):
    if difficulty == RAND:
        return get_nearest_grid( (random.randrange(0,WIDTH), random.randrange(0,HEIGHT)) )
    elif difficulty == EASY:
        # slow and toward the user
        x = userpos
        y = random.randrange(0, HEIGHT/2) #shoot toward the edge of the table
        
        return get_nearest_grid( (x,y) )
    elif difficulty == MEDIUM or difficulty == HARD:
        # slow and away from user
        x = WIDTH - userpos
        # map height to cos function
        theta = (float(x)/float(WIDTH)) * math.pi
        f_t = math.cos(theta-(math.pi/2.0))
        y = HEIGHT * f_t

        return get_nearest_grid( (x, y) )

def pick_speed(userpos, difficulty):
    if difficulty == RAND:
        return random.randrange(255)
    elif difficulty == EASY or difficulty == MEDIUM:
        return random.randrange(100)
    elif difficulty == HARD:
        return random.randrange(100,255)
