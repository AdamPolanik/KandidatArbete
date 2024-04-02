import ClimbingHoldDetector as holdDetector

image = holdDetector.openFile()

edges = holdDetector.findEdges(image)

holdDetector.draw(image, edges)

