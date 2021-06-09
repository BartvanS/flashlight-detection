# Python programe to illustrate
# simple thresholding type on an image

# organizing imports
import cv2
import numpy as np

def calc_light_pos(frame):
    # Our operations on the frame come here
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # ret, thresh1 = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)

    # Display the resulting frame
    lower_flashlight = np.array([30, 30, 255])
    upper_flashlight = np.array([179, 255, 255])
    mask = cv2.inRange(hsv, lower_flashlight, upper_flashlight)
    res = cv2.bitwise_and(frame,frame, mask= mask)
    # (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)
    # cv2.circle(frame, maxLoc, 50, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow('frame', res)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    calc_light_pos(frame)
    if cv2.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()