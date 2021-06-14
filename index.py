# Python programe to illustrate
# simple thresholding type on an image

# organizing imports
import cv2
import numpy as np
from time import time

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()


def calc_white_pixels():
    # Our operations on the frame come here
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return -1

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # ret, thresh1 = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)

    # Display the resulting frame
    lower_flashlight = np.array([0, 0, 255])
    upper_flashlight = np.array([179, 255, 255])
    mask = cv2.inRange(hsv, lower_flashlight, upper_flashlight)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    white_pixels = np.sum(res == 255)
    cv2.imshow('frame', res)
    return white_pixels


def calibrate():
    amount = 20
    pixel_count = 0
    for count in range(amount):
        pixel_count += calc_white_pixels()
    avg = pixel_count // amount
    thresh = avg + 500
    print(thresh)
    return int(thresh)


prev_time = time()


def process():
    white_pixels = calc_white_pixels()
    interval = 5
    global prev_time
    time_elapsed = time() - prev_time
    # print(white_pixels)
    if white_pixels >= threshold:
        prev_time = time()
        print("exceeded", prev_time)
    #     do light stuff
    elif time() - prev_time > interval:
        print("wuuutt")
        prev_time = time()
    #   do light slow down effects


if __name__ == "__main__":
    threshold = calibrate()
    while True:
        process()
        if cv2.waitKey(1) == ord('q'):
            break
        # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
