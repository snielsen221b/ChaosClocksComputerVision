#python color_tracking.py --video balls.mp4
#python color_tracking.py

#https://www.pyimagesearch.com/2015/09/21/opencv-track-object-movement/

# import the necessary packages
from __future__ import division
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import urllib #for reading image from
import time
import pickle


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
ap.add_argument("-p", "--picklename", type=str, default="testing.txt",
    help="data save name, ends in .txt")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the colors in the HSV color space
lower = {'blue':(100, 70, 50),'yellow':(18, 180, 130), 'red':(0, 170, 50),'green':(30, 90, 30)} #assign new item lower['blue'] = (93, 10, 0)
upper = {'blue':(110,255,255),'yellow':(54,255,255),'red':(15, 255, 255),'green':(86,220,255)}

# 19, 192, 114
# 25, 232,188

#For one video, red v max 180.  Had to change for another video

# define standard colors for circle around the object
colors = {'blue':(255,0,0),'yellow':(0, 200, 217),'red':(0,0,255),'green':(0, 255, 0)}

#Tracking center and time in an array

centers = []


#pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)
    print("using webcam")

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])
    print("using provided video")
# for i in range(430):
#     (grabbed, frame) = camera.read()
#     cv2.imshow("Frame",frame)
#     cv2.waitKey(1)

# Initialize time counting

frameno = -1
fps = camera.get(cv2.cv.CV_CAP_PROP_FPS)
print("fps =", fps)
# fps = camera.set(cv2.cv.CV_CAP_PROP_FPS,240)
# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
    # print(grabbed)
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        with open(args["picklename"], "wb") as fp:
            pickle.dump(centers, fp)
        # print(centers)
        break

    # Add frame count, time for each frame
    frameno = frameno + 1
    t = frameno*1/fps
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)

    blurred = cv2.GaussianBlur(frame, (11, 11), 0) #Increases time a bit
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    #for each color in dictionary check object in frame
    for key, value in upper.items():
        # construct a mask for the color from dictionary`1, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        kernel = np.ones((6,6),np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        # if key == "yellow":
        # cv2.imshow(key,mask)
        # waiting = cv2.waitKey() & 0xFF
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            for b in cnts:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                # print(c)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                # print(M)
                # print(frameno)
                # t = time.clock()

                # only proceed if the radius meets a minimum size. Correct this value for your obect's size
                if radius > 0.3:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
                    cv2.putText(frame,key + " ball", (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)
                    if M["m10"]:
                        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                        centers.append([key, center, t])
                    # save centers data in test.txt file
                    # with open("test3.txt", "wb") as fp:
                    #     pickle.dump(centers, fp)
                    # print(centers[-1])

    
    # for w in centers[i,:]:
    #     print(w)

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # print(frameno)
    if key == ord("s"):
        cv2.imwrite("testframe.png",hsv)
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        with open(args["picklename"], "wb") as fp:
            pickle.dump(centers, fp)
        # print(centers)
        break
    if key == ord("e"):
        # print(centers)
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
