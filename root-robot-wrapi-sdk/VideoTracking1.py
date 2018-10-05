from wrapi.py.devices.Root.Root_v1_0 import *
import threading
import cv2
import numpy as np
import math
import imutils

robot = Root_v1_0()

def drawSquare():
    distance = 10  # cm.

    robot.penDown()
    robot.move(distance)
    robot.rotate(90)
    robot.move(distance)
    robot.rotate(90)
    robot.move(distance)
    robot.rotate(90)
    robot.move(distance)
    robot.penAndEraserUp()
    robot.stop()


class ThreadDraw (threading.Thread):
    def run(self):
        drawSquare()

points = []
final_image = 0
raw_vals = []

cap = cv2.VideoCapture(0)  # USB camera (faster).
# cap = cv2.VideoCapture(1)  # Builtin camera (easier to position, plus simultaneous on-screen visualization).

ThreadDraw().start()


while True:
    # Load the current video image and make a copy of it for later
    ret, image = cap.read()
    #image = imutils.resize(image, width=1200)
    #image = imutils.resize(image, width=900)
    image = imutils.resize(image, width=600)  # Best FPS with the USB camera.

    ##middle_image = image.copy()
    # Convert image to HSV format
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Set boundries for green light
    greenLower = np.array([40, 60, 60])
    greenUpper = np.array([90, 255, 255])

    # Make a mask with the boundries and get rid of noise
    greenMask = cv2.inRange(hsv, greenLower, greenUpper)
    greenMask = cv2.erode(greenMask, None, iterations=1)
    greenMask = cv2.dilate(greenMask, None, iterations=1)

    # Find contours from first mask
    dummyImage, ledsContours, hierarchy = cv2.findContours(greenMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If contours exist the rest of this will be done
    if len(ledsContours) > 0:
        # Draw contours on copy image so they can be further analyzed
        addedContourColor = (255, 0, 0)
        cv2.drawContours(image, ledsContours, -1, addedContourColor, 12)

        # Make a new mask from the previous contours to get more data
        mask = cv2.inRange(image, addedContourColor, addedContourColor)
        mask = cv2.dilate(mask, None, iterations=5)
        dummyImage, addedContours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Make circle around all contours and find center point
        c = max(addedContours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        center = (int(x), int(y))
        cv2.circle(image, center, 5, (0, 255, 0), -1)

    cv2.imshow("RootTracking", image)

    # Quits when q is pressed:
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

# Release resources:
cap.release()
cv2.destroyWindow("RootTracking")
