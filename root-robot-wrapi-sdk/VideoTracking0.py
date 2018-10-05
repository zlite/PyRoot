#from wrapi.py.devices.Root.Root_v1_0 import *
import threading
import imutils

#robot = Root_v1_0()

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

## Code from Sara Lewis:

# import the necessary packages
import cv2
import numpy as np
import math

# Initialize variables that will be used in the program
points = []
final_image = 0
raw_vals = []

# Sets up video capture camera to main camera
#cap = cv2.VideoCapture(0)  # USB camera (faster).
cap = cv2.VideoCapture(1)  # Builtin camera (easier to position, plus simultaneous on-screen visualization).

#ThreadDraw().start()


while True:
    # Load the current video image and make a copy of it for later
    ret, image = cap.read()
    image = imutils.resize(image, width=1200)  # Best FPS with the USB camera.

#    image = image[100:800, 150:1200]
    middle_image = image.copy()
    # Convert image to HSV format
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Set boundries for green light
    lowerBound = np.array([40, 60, 60])
    upperBound = np.array([90, 255, 255])

    # Make a mask with the boundries and get rid of noise
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)

    # Find contours from first mask
    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If contours exist the rest of this will be done
    if len(contours)>0:
        # Draw contours on copy image so they can be further analyzed
        cv2.drawContours(middle_image, contours, -1, (0, 0, 255), 20)

        # Make a new mask from the previous red contours to get more data
        mask = cv2.inRange(middle_image, (0, 0, 250), (0, 0, 255))
        mask = cv2.dilate(mask, None, iterations=5)
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Make circle around all contours and find center point
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        center = (int(x), int(y))
        cv2.circle(image, center, 5, (0, 255, 0), -1)
        center = [int(x), int(y)]

        # Average past 2 points and update array
        if len(raw_vals) == 2:
            average_x = 0
            average_y = 0
            for i in range(len(raw_vals)):
                average_x += raw_vals[i][0]
                average_y += raw_vals[i][1]
            average_x = average_x/len(raw_vals)
            average_y = average_y/len(raw_vals)
            average_val = (average_x, average_y)
            points.append(average_val)
            raw_vals = []
        else:
            distance = 0
            if len(raw_vals) > 0:
                last_val = raw_vals[len(raw_vals)-1]
                distance = math.sqrt((center[0]-last_val[0])**2 + (center[1]-last_val[1])**2)
            if distance < radius*4:
                raw_vals.append(center)

#    Print the lines on the screen that represent previous movement
    for i in range(len(points)-1):
        cv2.line(image, points[i], points[i+1], (0, 255, 0), 60)
    for i in range(len(points)-1):
        cv2.line(image, points[i], points[i+1], (0, 0, 255), 5)

    cv2.imshow("Video", image)

    # Quit video if q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        final_image = image
        break

# When everything done, release the capture
cap.release()
cv2.destroyWindow("Video")

# Show final picture with tracking
cv2.imshow("Final image", final_image)
cv2.waitKey(0)
