import cv2
import numpy as np
import time as t
import img_processing
import calculation
capture = cv2.VideoCapture(0)

frame_hight = 10
frame_width = 10

capture.set(3, frame_width)
capture.set(4, frame_hight)
capture.set(10, 150)
frame_rate = 1
prev = 0
_, shape = capture.read()

while True:
    time_elapsed = t.time() - prev

    isTrue, frame = capture.read()

    if time_elapsed > 1 / frame_rate:
        img_result = frame.copy()
        img_corner = frame.copy() 
        prev = t.time()
        result = img_processing.imgprocess(frame)
        corner  = calculation.findcontours(result,frame)
        cv2.imshow('Video0', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
capture.release()
cv2.destroyAllWindows()
