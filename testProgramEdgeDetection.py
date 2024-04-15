import cv2
import ClimbingHoldDetector as holdDetector
import time
import matplotlib.pyplot as plt
from utility import isInBox, open_images_and_coordinates

plotPoints = []

start_time = time.time()

totalAccuracy = 0

pictureFolderPath = "/home/addedoom/skola/Climbing Holds and Volumes.v14i.yolov8/test/images_and_labels/"
image_data = open_images_and_coordinates(pictureFolderPath)

detectedHoldsFromModel, timePlotPoints = holdDetector.openImagesForModel(pictureFolderPath)

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
        currentAccuracy = (amountOfCorrectIdentifications/len(coordinates))
        totalAccuracy += currentAccuracy

        plotPoints.append([0,currentAccuracy])

else:
    print("No images or coordinates found in the specified folder.")

totalAccuracy = (totalAccuracy/len(detectedHoldsFromModel))
print("EDGE_DETECTION_MODEL> Total accuracy of model: ", totalAccuracy, " amount of images used: ", len(detectedHoldsFromModel))

end_time = time.time()

runtime = end_time - start_time
print(f"Runtime: {runtime:.2f} seconds")

plt.figure(1)
plt.xlabel('Image')
plt.ylabel('Accuracy (0-1)')
plt.title('Detection accuracy per Image')
plt.suptitle('Edge-detection Model')
plt.grid(True)
plt.plot(plotPoints)

sum = 0

for accuracy in plotPoints:
    sum += accuracy[1]

# Calculate the average time
averageAccuracy = (sum / len(plotPoints))
plt.axhline(y=round(averageAccuracy, 3), color='g', linestyle='--', label='Average Accuracy (' + str(round(averageAccuracy, 3)) + ')')
plt.legend()

plt.figure(2)
plt.xlabel('Image')
plt.ylabel('Time (seconds)')
plt.title('Processing time per Image')
plt.suptitle('Edge-detection Model')
plt.grid(True)
plt.plot(timePlotPoints)

sum = 0

for time in timePlotPoints:
    sum += time[1]

# Calculate the average time
averageTime = (sum / len(timePlotPoints))

plt.axhline(y=round(averageTime, 3), color='g', linestyle='--', label='Average Time (' + str(round(averageTime, 3)) + ')')

plt.legend()

plt.show()

