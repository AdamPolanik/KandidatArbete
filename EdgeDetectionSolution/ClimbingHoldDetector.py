import os
from utility import choose_picture, openImage, displayImage, BoundingBox
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

"""Misc functions to open picture"""

def openFile():
    filePath = choose_picture()
    image = openImage(filePath)
    resizeImage(image)

    return image

def resizeImage(image):
    # Resizing image to speed up processing
    c = 1000.0/image.shape[0]
    x = int(image.shape[0] * c)
    y = int(image.shape[1] * c)
    image = cv2.resize(image, (y,x))
    return image

"""Computational functions calculating where holds are located"""

def findEdges(image):

    # Applies a gaussianBlur with a 5x5 kernel size to reduce noise and smooth out edges. 
    blurredImage = cv2.GaussianBlur(image, (5, 5), 0)

    # Convert the image to grayscale
    grayImage = cv2.cvtColor(blurredImage, cv2.COLOR_BGR2GRAY)

    # Applies Otsu's thresholding method to choose threshold values.
    threshold, _ = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # print(threshold)

    # Applies Canny edge detection to find edges separating holds from the wall.
    edges = cv2.Canny(blurredImage, 100, 100 * 2, L2gradient=True)


    # !!!Adjust code under this comment to change accuracy!!!


    # Finds the contours of the image, discarding hierarchy (test with cv2.RETR_TREE)
    contours, _ = cv2.findContours(edges,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    # Applies convex hulls to each contour, ensuring each contour is a closed polygon. 
    hulls = list(map(cv2.convexHull,contours))

    # Creates an empty (black) canvas and draws the contours (white) onto it.
    mask = np.zeros(image.shape, np.uint8)
    cv2.drawContours(mask, hulls, -1, [255,255,255], -1)

    # Under this comment is 3 different ways of extracting keypoints, don't know which one is the best right now.

    # # Apply dilation to fill in the outlines
    # kernel = np.ones((5,5),np.uint8)

    # closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # dilated = cv2.dilate(edges, kernel, iterations = 1)

    # blobDetectorTest = buildDetector()
    # keypointsTest = blobDetectorTest.detect(dilated)

    # blobDetectorTest3 = buildDetector()
    # keypointsTest3 = blobDetectorTest3.detect(closed_edges)

    # Utilising simpleblobtdetector on the mask to define keypoints (Original way).
    blobDetector = buildDetector()
    keypoints = blobDetector.detect(mask)

    # drawImage(closed_edges, "Image showing closedEdges using morphology")

    # drawImage(mask, "Image showing convexHullMask")

    # # Debug purpose, shows the image representing the dialated-mask.
    # drawImage(dilated, "Image showing dialation")


    # # Convert the image to grayscale
    # grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # # Create a black and white image with the keypoints
    # keypointsImage = cv2.drawKeypoints(grayImage, keypointsTest, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # # Debug purpose, shows the image representing the Keypoints.
    # drawImage(keypointsImage, "Image showing dialated-keypoints using edge-dialation")

    # # Create a black and white image with the keypoints
    # keypointsImage = cv2.drawKeypoints(grayImage, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # # Debug purpose, shows the image representing the Keypoints.
    # drawImage(keypointsImage, "Image showing keypoints using no dialation")

    # # Create a black and white image with the keypoints
    # keypointsImage = cv2.drawKeypoints(grayImage, keypointsTest3, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # # Debug purpose, shows the image representing the Keypoints.
    # drawImage(keypointsImage, "Image showing keypoints using morphology")

    # draw(image, keypointsTest3)

    return keypoints


def buildDetector(minArea = 25):
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Thresholds for back and white image
    params.minThreshold = 0
    params.maxThreshold = 255

    # Exclude blobs smaller than minArea (to reduce false selection based on noise in image)
    params.filterByArea = True
    params.minArea = minArea

    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0.1
        
    # Filter by Inertia, meaning elongated holds are excluded (values less than 0.05)
    params.filterByInertia = True
    params.minInertiaRatio = 0.05

    # Create a detector with the parameters
    ver = (cv2.__version__).split('.')
    if int(ver[0]) < 3 :
        detector = cv2.SimpleBlobDetector(params)
    else : 
        detector = cv2.SimpleBlobDetector_create(params)

    return detector


"""Functions to show the resuls in image format"""

# Draws bounding boxes around each hold according to keypoints information.
def draw(img, keypoints):

    # List that holds the coordinates for each boundingBox
    boundingBoxes = []

    for i, key in enumerate(keypoints):
        # Gets the x and y coordinates for the keypoint
        x = int(key.pt[0])
        y = int(key.pt[1])

        # Gets the size by rounding up the diameter 
        size = int(math.ceil(key.size)) 

        #Finds a rectangular window in which the keypoint fits
        bottomRight = (x + size, y + size)   
        topLeft = (x - size, y - size)

        boundingBox = BoundingBox(bottomRight,topLeft)

        # Adds coordinates for boundingBox to list
        boundingBoxes.append(boundingBox)

        # Draws a rectangle around the keypoint
        cv2.rectangle(img, topLeft, bottomRight, (0,0,255), 2)

    # Displays the results
    # drawImage(img, "Image with boundingBoxes")
    
    return boundingBoxes

def drawImage(image, title):
    displayImage(image, title)


def openImagesForModel(folder_path):
    imageData = {}

    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return None

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):

        # Check for valid image extensions
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            
            # print("filename inside .jpg:    ", filename)
            image_path = os.path.join(folder_path, filename)

            # print("Image path: ", image_path)
            try:
                image = cv2.imread(image_path, 1)  # Read in color mode

            except (cv2.error, FileNotFoundError) as e:
                print(f"Error opening image '{image_path}': {e}")
                image = None
            boundingboxes = []

            edges = findEdges(image)
            boundingboxes = draw(image, edges)

            imageData[image_path] = boundingboxes

    return imageData
