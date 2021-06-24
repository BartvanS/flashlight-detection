import cv2
import numpy as np
from time import time, sleep

import serial

ser = serial.Serial('/dev/ttyACM0')
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()


def ser_write(val):
    ser.write(val.encode())


def get_frame_grayscale():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return -1
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Display the resulting frame
    lower_flashlight = np.array([0, 0, 200])
    upper_flashlight = np.array([179, 255, 255])
    mask = cv2.inRange(hsv, lower_flashlight, upper_flashlight)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    return res


def calc_white_pixels(frame):
    white_pixels = np.sum(frame == 255)
    return white_pixels


def calibrate(frame):
    amount = 20
    pixel_count = 0
    for count in range(amount):
        pixel_count += calc_white_pixels(frame)
    avg = pixel_count // amount
    thresh = avg + 1000
    print("done calibrating.")
    return int(thresh)


prev_time = time()


def process(frame):
    white_pixels = calc_white_pixels(frame)
    interval = 5
    global prev_time
    time_elapsed = time() - prev_time
    if white_pixels >= threshold:
        prev_time = time()
        print("past threshold")
        ser_write("a")
        sleep(1)
    #     do light stuff
    elif time_elapsed > interval:
        print("wuuutt")
        prev_time = time()
        ser_write("b")
    #   do slow down effects


if __name__ == "__main__":
    threshold = calibrate(get_frame_grayscale())
    while True:
        frame = get_frame_grayscale()
        process(frame)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) == ord('q'):
            break
        # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    ser.close()
