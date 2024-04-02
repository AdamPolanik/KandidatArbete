from tkinter import filedialog
from tkinter import Tk
import matplotlib.pyplot as plt
import cv2
import numpy as np


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

def displayImage(image, title):
    # Used for debug purpose
    # print(image.dtype)

    # converts the image to rgb from bgr before display
    convertedImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    plt.imshow(convertedImage)
    plt.axis('off')
    plt.title(title)
    plt.show()

