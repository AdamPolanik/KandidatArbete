import os
from utility import choose_picture, openImage, displayImage, BoundingBox
import cv2
import math
import time
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

    # # Applies Canny edge detection to find edges separating holds from the wall.
    # edges = cv2.Canny(blurredImage, threshold, threshold * 2, L2gradient=False)

    # # Finds the contours of the image, discarding hierarchy (test with cv2.RETR_TREE)
    # contours, _ = cv2.findContours(edges,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


    # Convert the image to HSV color space
    hsvImage = cv2.cvtColor(blurredImage, cv2.COLOR_BGR2HSV)

    # Define color ranges for climbing holds
    color_ranges = [
        ((40, 50, 50), (80, 255, 255)),   # Green
        ((0, 100, 100), (10, 255, 255)),  # Red (Part 1)
        ((170, 100, 100), (180, 255, 255)),  # Red (Part 2)
        ((120, 50, 50), (160, 255, 255)),  # Purple
        ((20, 100, 100), (40, 255, 255)),  # Yellow
        ((90, 50, 50), (130, 255, 255))   # Blue
    ]


    # Create binary masks for each color range
    masks = []
    for color_range in color_ranges:
        lower_color, upper_color = color_range
        mask = cv2.inRange(hsvImage, lower_color, upper_color)
        masks.append(mask)


    # Initialize an empty mask
    combined_mask = np.zeros_like(masks[0])

    # Combine binary masks using bitwise OR operation
    for mask in masks:
        combined_mask = cv2.bitwise_or(combined_mask, mask)

    # Apply Canny edge detection on the original image
    edges = cv2.Canny(blurredImage, threshold, threshold * 2, L2gradient=False)

    # Perform morphological operations to improve blob detection
    # kernel = np.ones((5, 5), np.uint8)
    # dilated_edges = cv2.dilate(edges, kernel, iterations=2)

    # Combine color segmentation and edge detection results
    combined_edges = cv2.bitwise_and(combined_mask, edges)

    # Finds the contours of the image, discarding hierarchy (test with cv2.RETR_TREE)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)




    # Applies convex hulls to each contour, ensuring each contour is a closed polygon. 
    hulls = list(map(cv2.convexHull, contours))

    # Creates an empty (black) canvas and draws the contours (white) onto it.
    mask = np.zeros(image.shape, np.uint8)
    cv2.drawContours(mask, hulls, -1, [255,255,255], -1)


    # drawImage(image, "original image")
    # drawImage(combined_mask, "color segmentation")
    # drawImage(edges, "edge detection")
    # drawImage(combined_edges, "combination")
    # drawImage(dilated_image, "combined with morphological operations")

    # Utilising simpleblobtdetector on the mask to define keypoints.
    blobDetector = buildDetector()
    keypoints = blobDetector.detect(mask)

    # drawBoundingboxes(image,keypoints)

    return keypoints


def buildDetector(minArea = 20):
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Thresholds for back and white image
    params.minThreshold = 0
    params.maxThreshold = 255

    params.filterByColor = True
    params.blobColor = 255 

    # Exclude blobs smaller than minArea (to reduce false selection based on noise in image)
    params.filterByArea = True
    params.minArea = minArea

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = True
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
def drawBoundingboxes(img, keypoints):

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
    # drawImage(img, "Edge-detection")
    
    return boundingBoxes

def drawImage(image, title):
    displayImage(image, title)

def openImagesForModel(folder_path):
    imageData = {}
    timePlotPoints = []

    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return None

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):

        # Check for valid image extensions
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            
            image_path = os.path.join(folder_path, filename)
            image = openImage(image_path)

            boundingboxes = []

            start = time.time()

            edges = findEdges(image)
            boundingboxes = drawBoundingboxes(image, edges)

            end = time.time()

            timeSpent = end - start

            timePlotPoints.append(timeSpent)

            imageData[image_path] = boundingboxes

    return imageData, timePlotPoints
