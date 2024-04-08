import cv2
import ClimbingHoldDetector as holdDetector
import time
from utility import isInBox, open_images_and_coordinates, openImage, displayImage

start_time = time.time()

totalAccuracy = 0

pictureFolderPath = "/home/addedoom/skola/Climbing Holds and Volumes.v14i.yolov8/test/images_and_labels/"
image_data = open_images_and_coordinates(pictureFolderPath)

detectedHoldsFromModel = holdDetector.openImagesForModel(pictureFolderPath)

if detectedHoldsFromModel is not None:
    # Process the dictionary containing coordinates:
    for filePath, boundingBox in detectedHoldsFromModel.items():
        amountOfCorrectIdentifications = 0
        # Check if coordinates loaded successfully
        coordinates = image_data.get(filePath)
        maxAmountOfHolds = len(coordinates)

        for box in boundingBox:
            for cord in coordinates:
                if (isInBox(box, cord)):
                    if (amountOfCorrectIdentifications < maxAmountOfHolds):
                        amountOfCorrectIdentifications += 1
                    else:
                        break
        # print(amountOfCorrectIdentifications, " out of ", len(coordinates), " accuracy of: ", f"{amountOfCorrectIdentifications/len(coordinates):.5f}")
        totalAccuracy += (amountOfCorrectIdentifications/len(coordinates))
else:
    print("No images or coordinates found in the specified folder.")

totalAccuracy = (totalAccuracy/len(detectedHoldsFromModel))
print("EDGE_DETECTION_MODEL> Total accuracy of model: ", totalAccuracy, " amount of images used: ", len(detectedHoldsFromModel))

end_time = time.time()

runtime = end_time - start_time
print(f"Runtime: {runtime:.2f} seconds")

# if image_data is not None:
#     # Process the dictionary containing coordinates:
#     for image_name, coords in image_data.items():
#         # Check if coordinates loaded successfully
#         if coords:
#             print(f"filename: {image_name}")
#             # Print formatted x and y for each coordinate
#             for x, y in coords:
#                 print(f"Center: ({x}, {y})")
#         else:
#             print(f"Error loading coordinates for '{image_name}'.")
# else:
#     print("No images or coordinates found in the specified folder.")


# first_filepath = next(iter(image_data))

# coordinates = image_data.get(first_filepath)

# image = openImage(first_filepath)

# for x, y in coordinates:
#         # Define circle parameters (adjust radius as needed)
#         circle_radius = 10  # Adjust as desired
#         circle_color = (0, 0, 255)  # Blue color (BGR)
#         circle_thickness = 2  # Thickness of the circle

#         # Draw circle on the image
#         cv2.circle(image, (x, y), circle_radius, circle_color, circle_thickness)

# # Displays the results
# displayImage(image, "Image with coordinates")

# image = holdDetector.openFile()

# edges = holdDetector.findEdges(image)

# boundingboxes = holdDetector.draw(image, edges)

# # for bounding_box in boundingboxes:
# #     print(f"\tTop-left: ({bounding_box.topLeft[0]}, {bounding_box.topLeft[1]})")
# #     print(f"\tBottom-right: ({bounding_box.bottomRight[0]}, {bounding_box.bottomRight[1]})")

# # Checks if a given point is in a boundingBox (used for accuracy testing)
# print(isInBox(boundingboxes[0],[30,1025]))
