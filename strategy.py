import numpy as np
import cv2


def get_nearest_grid(point, width, height, spacing):
    xs = np.arange(20,width, spacing)
    ys = np.arange(20, height, spacing)[:-2]
    x_i = (np.abs(xs - point[0])).argmin()
    y_i = (np.abs(ys - point[1])).argmin()

    return xs[x_i], ys[y_i]
