import cv2 
import numpy as np
def grid_line_helper(img, shape_location, length=10):
    clone = img.copy()
    # if its horizontal lines then it is shape_location 1, for vertical it is 0
    row_or_col = clone.shape[shape_location]
    # find out the distance the lines are placed
    size = row_or_col // length

    # find out an appropriate kernel
    if shape_location == 0:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, size))
    else:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, 1))

    # erode and dilate the lines
    clone = cv2.erode(clone, kernel)
    clone = cv2.dilate(clone, kernel)

    return clone
def get_grid_lines(img, length=10):
    horizontal = grid_line_helper(img, 1, length)
    vertical = grid_line_helper(img, 0, length)
    return vertical, horizontal    