import cv2
import operator
import numpy as np

def findcontours(img, original):
    # find contours on thresholded image
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # sort by the largest
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    polygon = None

    # make sure this is the one we are looking for
    for cnt in contours:
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, closed=True)
        approx = cv2.approxPolyDP(cnt, 0.01 * perimeter, closed=True)
        num_corners = len(approx)
        if num_corners == 4 and area > 1000:
            polygon = cnt
            break

    if polygon is not None:
        # find its extreme corners
        top_left = find_extreme_corners(polygon, min, np.add)  # has smallest (x + y) value
        top_right = find_extreme_corners(polygon, max, np.subtract)  # has largest (x - y) value
        bot_left = find_extreme_corners(polygon, min, np.subtract)  # has smallest (x - y) value
        bot_right = find_extreme_corners(polygon, max, np.add)  # has largest (x + y) value

        # if its not a square, we don't want it
        if bot_right[1] - top_right[1] == 0:
            return []
        if not (0.95 < ((top_right[0] - top_left[0]) / (bot_right[1] - top_right[1])) < 1.05):
            return []

        cv2.drawContours(original, [polygon], 0, (0, 0, 255), 3)

        # draw corresponding circles
        [draw_extreme_corners(x, original) for x in [top_left, top_right, bot_right, bot_left]]

        return [top_left, top_right, bot_right, bot_left]

    return []
def find_extreme_corners(polygon, limit_fn, compare_fn):
    # limit_fn is the min or max function
    # compare_fn is the np.add or np.subtract function
    section, _ = limit_fn(enumerate([compare_fn(pt[0][0], pt[0][1]) for pt in polygon]),key=operator.itemgetter(1))
    return polygon[section][0][0], polygon[section][0][1]    

def draw_extreme_corners(pts, original):
    cv2.circle(original, pts, 5, (0, 255, 0), cv2.FILLED)

def cut_extra_image(corners, original):
    # we will be warping these points
    corners = np.array(corners, dtype='float32')
    
    top_left, top_right, bot_right, bot_left = corners
    
    # find the best side width, since we will be warping into a square, height = length
    width = int(max([np.linalg.norm(top_right - bot_right),np.linalg.norm(top_left - bot_left),np.linalg.norm(bot_right - bot_left),np.linalg.norm(top_left - top_right)]))
    #print(np.linalg.norm(top_right - bot_right),top_right - bot_right,np.linalg.norm(top_left - bot_left),top_left - bot_left,np.linalg.norm(bot_right - bot_left),bot_right - bot_left,np.linalg.norm(top_left - top_right),top_left - top_right,width)
    # create an array with shows top_left, top_right, bot_left, bot_right
    mapping = np.array([[0, 0], [width - 1, 0], [width - 1, width - 1], [0, width - 1]], dtype='float32')

    matrix = cv2.getPerspectiveTransform(corners, mapping)
    
    return cv2.warpPerspective(original, matrix, (width, width))   