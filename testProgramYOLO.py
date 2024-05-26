import time
import yoloHelper as yolo
import matplotlib.pyplot as plt
from utility import isInBox, open_images_and_coordinates, displayImage, openImage, colors

correctHoldPlotPoints = []
correctBoxPlotPoints = []
totalAccuracyPlotPoints = []

start_time = time.time()

totalAccuracy = 0

# Path to test-folder (should contain image + textfile combination, with the same name, in yolo-format, for each image in the folder)
pictureFolderPath = "Path_to_images_and_textfiles_containing_information_about_holdplacement"
image_data = open_images_and_coordinates(pictureFolderPath)

# Does the detection for each image in the folder
detectedHoldsFromModel, timePlotPoints = yolo.openImagesForModel(pictureFolderPath)

# The code below calculates performance mesurements for the model
if detectedHoldsFromModel is not None:
    # Process the dictionary containing coordinates:
    for filePath, boundingBox in detectedHoldsFromModel.items():

        amountOfCorrectIdentifications = 0
        amountOfDoubleIdentifications = 0
        incorrectIdentifications = 0
        # Check if coordinates loaded successfully
        coordinates = image_data.get(filePath)
        maxAmountOfHolds = len(coordinates)

        for box in boundingBox:
            for cord in coordinates:
                if (isInBox(box, cord)):
                    amountOfCorrectIdentifications += 1
                    coordinates.remove(cord)
                    break
                    
        correctlyIdentifiedHolds = (amountOfCorrectIdentifications/maxAmountOfHolds)
        incorrectIdentifications = ((len(boundingBox) - amountOfCorrectIdentifications)) / len(boundingBox)
        correctIdentifications = 1 - incorrectIdentifications
        currentAccuracy = correctlyIdentifiedHolds * correctIdentifications
        totalAccuracy += currentAccuracy

        # To find out which pictures the model performs bad on
        # if (currentAccuracy < 0.5):
        #     displayImage(openImage(filePath), "Image with trash accuracy")

        correctHoldPlotPoints.append(correctlyIdentifiedHolds)
        correctBoxPlotPoints.append(correctIdentifications)
        totalAccuracyPlotPoints.append(currentAccuracy)

else:
    print("No images or coordinates found in the specified folder.")



"""For showing results and ploting graphs"""

totalAccuracy = (totalAccuracy/len(detectedHoldsFromModel))
print("YOLO_MODEL> Total accuracy of model: ", totalAccuracy, " amount of images used: ", len(detectedHoldsFromModel))

end_time = time.time()

runtime = end_time - start_time
print(f"Runtime: {runtime:.2f} seconds")


sum = 0
for accuracy in correctHoldPlotPoints:
    sum += accuracy
averageHoldAccuracy = (sum / len(correctHoldPlotPoints))

sum = 0
for accuracy in correctBoxPlotPoints:
    sum += accuracy
averageBoxAccuracy = (sum / len(correctBoxPlotPoints))

sum = 0
for accuracy in totalAccuracyPlotPoints:
    sum += accuracy
averageAccuracy = (sum / len(totalAccuracyPlotPoints))

sum = 0
for times in timePlotPoints:
    sum += times
averageTime = (sum / len(timePlotPoints))


fig, axs = plt.subplots(2, 2, figsize=(12, 10))
axs[0, 0].plot(
    correctHoldPlotPoints, color=colors[4], linestyle="-", label="Hold accuracy"
)
axs[0, 0].axhline(
    y=round(averageHoldAccuracy, 3),
    color='g', 
    linestyle='--', 
    label='Average accuracy (' + str(round(averageHoldAccuracy, 3)) + ')'
    )

axs[0, 0].set_xlabel("Image")
axs[0, 0].set_ylabel("Identification accuracy")
axs[0, 0].set_title("Correctly identified holds")
axs[0, 0].legend()

axs[0, 1].plot(
    correctBoxPlotPoints, color=colors[1], linestyle="-", label="Boundingbox accuracy"
)
axs[0, 1].axhline(
    y=round(averageBoxAccuracy, 3),
    color='g', 
    linestyle='--', 
    label='Average accuracy (' + str(round(averageBoxAccuracy, 3)) + ')'
    )

axs[0, 1].set_xlabel("Image")
axs[0, 1].set_ylabel("Identification accuracy")
axs[0, 1].set_title("Correctly placed boundingboxes")
axs[0, 1].legend()

axs[1, 0].plot(
    timePlotPoints, color=colors[2], linestyle="-", label="Time (s)"
)
axs[1, 0].axhline(
    y=round(averageTime, 3),
    color='g', 
    linestyle='--', 
    label='Average time (' + str(round(averageTime, 3)) + ')'
    )

axs[1, 0].set_xlabel("Image")
axs[1, 0].set_ylabel("Time (s)")
axs[1, 0].set_title("Execution time")
axs[1, 0].legend()

axs[1, 1].plot(
    totalAccuracyPlotPoints, color=colors[3], linestyle="-", label="Accuracy"
)
axs[1, 1].axhline(
    y=round(averageAccuracy, 3),
    color='g', 
    linestyle='--', 
    label='Average accuracy (' + str(round(averageAccuracy, 3)) + ')'
    )

axs[1, 1].set_xlabel("Image")
axs[1, 1].set_ylabel("Accuracy")
axs[1, 1].set_title("Total model Accuracy")
axs[1, 1].legend()

plt.suptitle("YOLO model")
plt.legend()
plt.show()

# plt.savefig("YOLO-plot.png")