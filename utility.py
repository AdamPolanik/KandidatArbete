from tkinter import filedialog
from tkinter import Tk
import matplotlib.pyplot as plt
import cv2
import os

colors = ["#f6b3d3", "#e4026f", "#009ce9", "#1ca884", "#ffba13"]

def choose_picture():
    # Create a Tkinter root window
    root = Tk()
    root.withdraw()  # Hide the root window

    # Open the file dialog
    file_path = filedialog.askopenfilename()

    return file_path

def openImage(file_path = None):
    # If no file path given, open dialog
    if file_path is None:
        file_path = choose_picture()
    
    # If stil no file path chosen, quit
    if file_path == None:
        return None

    image = cv2.imread(file_path,1)
    return image


def open_images_and_coordinates(folder_path):

    image_data = {}
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return None

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):

        # Check for valid image extensions
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            
            # print("filename inside .jpg:    ", filename)
            image_path = os.path.join(folder_path, filename)

            image = openImage(image_path)

            changedExtention = image_path[:-3]
            coord_path = changedExtention + "txt"
            coordinates = []
            try:
                with open(coord_path, 'r') as f:

                    # Extract and process all remaining coordinates
                    for line in f:  # Iterate through all lines
                        line = line.strip()
                        _, x_center_normalized, y_center_normalized, _, _ = map(float, line.split())

                        if image is not None:
                            x = int(x_center_normalized * image.shape[1])
                            y = int(y_center_normalized * image.shape[0])
                            # print("Coordinates for image: ", x, " ", y)
                            
                            coordinates.append((x, y))
            except (FileNotFoundError, ValueError, StopIteration) as e:
                print(f"Error reading coordinates for '{filename}': {e}")

            image_data[image_path] = coordinates

    return image_data

def displayImage(image, title):

    # converts the image to rgb from bgr before display
    convertedImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    plt.imshow(convertedImage)
    plt.axis('off')
    plt.title(title)
    plt.show()

# Function to calculate accuracy (if a given point is in a boundingBox)
def isInBox(boundingBox, point):
    x, y = point
    topLeftX, topLeftY = boundingBox.topLeft
    bottomRightX, bottomRightY = boundingBox.bottomRight

    # if ((topLeftX <= x <= bottomRightX) and (topLeftY <= y <= bottomRightY)):
        
    # Check if the point is within the horizontal and vertical boundaries of a box at a choosen subarea of the boundingbox
    return isCorrectBoundingbox(topLeftX, topLeftY, bottomRightX, bottomRightY, x, y)

def isCorrectBoundingbox(topLeftX, topLeftY, bottomRightX, bottomRightY, pointX, pointY):

    xLength = (abs(topLeftX - bottomRightX)/2)
    yLength = (abs(topLeftY - bottomRightY)/2)

    # How big the box should be compared to the boundingbox
    checkAreaProcentage = 0.5

    xLength = xLength*checkAreaProcentage
    yLength = yLength*checkAreaProcentage

    rightX = pointX + xLength
    leftX = pointX - xLength
    topY = pointY + yLength
    bottomY = pointY - yLength

    # if ((topLeftX <= (leftX and rightX) <= bottomRightX) and (topLeftY <= (bottomY and topY) <= bottomRightY))

    if((topLeftX <= leftX  <= bottomRightX)):
        if ((topLeftX <= rightX <= bottomRightX)):
            if ((topLeftY <= bottomY  <= bottomRightY)):
                if ((topLeftY <= topY <= bottomRightY)):
                    return True
    return False

class BoundingBox:
    def __init__(self, bottomRight, topLeft):
        self.bottomRight = bottomRight
        self.topLeft = topLeft
    

def open_images(folder_path):

    images = []
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return None

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):

        # Check for valid image extensions
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            
            # print("filename inside .jpg:    ", filename)
            image_path = os.path.join(folder_path, filename)

            image = openImage(image_path)
            images.append(image)
    
    return images