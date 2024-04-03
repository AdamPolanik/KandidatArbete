import ClimbingHoldDetector as holdDetector
from utility import isInBox

image = holdDetector.openFile()

edges = holdDetector.findEdges(image)

boundingboxes = holdDetector.draw(image, edges)

# for bounding_box in boundingboxes:
#     print(f"\tTop-left: ({bounding_box.topLeft[0]}, {bounding_box.topLeft[1]})")
#     print(f"\tBottom-right: ({bounding_box.bottomRight[0]}, {bounding_box.bottomRight[1]})")

# Checks if a given point is in a boundingBox (used for accuracy testing)
print(isInBox(boundingboxes[0],[30,1025]))

