from ultralytics import YOLO
import os
import time
import cv2
from utility import openImage, BoundingBox, displayImage

model = YOLO("YOLOV8MODEL_60EPOCHS.pt")

def getBoundingboxes(results, image):
    boxes = []

    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy.tolist()[0]

        topLeft = (int(x1), int(y1))
        bottomright = (int(x2), int(y2))

        # to print boundingbox
        cv2.rectangle(image, topLeft, bottomright, (0,0,255), 2)

        box = BoundingBox(bottomright, topLeft)

        boxes.append(box)

    # to show image
    #displayImage(image, "YOLO")

    return boxes

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

            results = model(image)
            boundingboxes = getBoundingboxes(results, image)

            end = time.time()

            timeSpent = end - start

            timePlotPoints.append(timeSpent)

            imageData[image_path] = boundingboxes

    return imageData, timePlotPoints