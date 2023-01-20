import cv2
import time as t

capture = cv2.VideoCapture(0)

frame_hight = 10
frame_width = 10

capture.set(3, frame_width)
capture.set(4, frame_hight)
capture.set(10, 150)
frame_rate = 30
prev = 0

while True:
    time_elapsed = t.time() - prev

    isTrue, frame = capture.read()

    if time_elapsed > 1 / frame_rate:

        prev = t.time()
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #blur = cv2.GaussianBlur(img_gray, (9, 9), 0)
        cv2.imshow('Video', img_gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
capture.release()
cv2.destroyAllWindows()
