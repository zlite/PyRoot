import threading
import cv2
import numpy as np
import math
import imutils
from wrapi.py.devices.Root.Root_v1_0 import *

robot = Root_v1_0()


def drawSquare():
    distance = 10  # cm.

    # robot.penDown()
    robot.move(distance)
    robot.rotate(90)
    robot.move(distance)
    robot.rotate(90)
    robot.move(distance)
    robot.rotate(90)
    robot.move(distance)
    # robot.penAndEraserUp()
    robot.stop()


class ThreadDraw (threading.Thread):
    def run(self):
        drawSquare()


trackingColor = (0, 255, 0)
camera = cv2.VideoCapture(0)  # USB camera (faster).
# camera = cv2.VideoCapture(1)  # Builtin camera (easier to position, plus simultaneous on-screen visualization).


def trackRobot(image, color):
    # Convert image to HSV format:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Set boundries for green light:
    greenLower = np.array([40, 60, 60])
    greenUpper = np.array([90, 255, 255])

    # Make a mask with the boundries and get rid of noise
    greenMask = cv2.inRange(hsv, greenLower, greenUpper)
    greenMask = cv2.erode(greenMask, None, iterations=1)
    greenMask = cv2.dilate(greenMask, None, iterations=1)

    # Find contours from first mask:
    dummyImage, ledsContours, hierarchy = cv2.findContours(greenMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(ledsContours) > 0:
        addedContourColor = (255, 0, 0)
        cv2.drawContours(image, ledsContours, -1, addedContourColor, 12)

        # Make a new mask from the previous contours to improve tracking:
        mask = cv2.inRange(image, addedContourColor, addedContourColor)
        mask = cv2.dilate(mask, None, iterations=5)
        dummyImage, addedContours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Make circle around all contours and find center point:
        c = max(addedContours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        center = (int(x), int(y))
        cv2.circle(image, center, 5, color, -1)
        # cv2.circle(image, center, int(radius*2), (0, 255, 0), 2)

    return image, center, radius


def drawTracking(image, center, radius, points, values, color):
    # Average past 2 points and update array
    if len(values) == 2:
        averageX = 0
        averageY = 0
        for i in range(len(values)):
            averageX += values[i][0]
            averageY += values[i][1]
        averageX = averageX / len(values)
        averageY = averageY / len(values)
        averageVal = (averageX, averageY)
        points.append(averageVal)
        values = []
    else:
        distance = 0
        if len(values) > 0:
            lastVal = values[len(values) - 1]
            distance = math.sqrt((center[0] - lastVal[0])**2 + (center[1] - lastVal[1])**2)
        if distance < radius * 4:
            values.append(center)

    for i in range(len(points)-1):
        cv2.line(image, points[i], points[i+1], color, 5)

    return image, points, values


ThreadDraw().start()
globalPoints = []
globalValues = []
while True:
    # Capture the current image from the camera, and resize it to improve processing speed:
    ret, image = camera.read()
    image = imutils.resize(image, width=600)  # Best FPS with the USB camera.
    # image = imutils.resize(image, width=900)
    # image = imutils.resize(image, width=1200)

    # Process image:
    image, center, radius = trackRobot(image, trackingColor)
    image, globalPoints, globalValues = drawTracking(image, center, radius, globalPoints, globalValues, trackingColor)

    # Show image:
    cv2.imshow("RootTracking", image)

    # Quits when q is pressed:
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

# Release resources:
camera.release()
cv2.destroyWindow("RootTracking")
