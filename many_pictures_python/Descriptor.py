"""
instead of comparing each video frame with a Input image slice we will place them into so called bins.
We will determine which frame goes into which bin depending on their color values.
The frames will be converted form the initial color scheme Blue,Green,Red into Hue,Saturation and Value.
Each Color Value gets a different amount of bins. Exmaple Hue: 8 Saturation: 12 Value: 3
A frame will be saved as a combination of 3 values refering the Bin each of its color values belongs to.
Now we compare the Input Image Slice with pictures with the same Bin combination instead with every picture.
"""
import cv2 as cv

class Descriptor:

    def __init__(self, bins):
        "save how many bins for each Color Value"
        self.bins = bins

    def describe(self, frame):
        "Convert color scheme"
        frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        features = []
        
        hist = cv.calcHist(frame, [1, 2, 3], None, self.bins, [0, 180, 0, 256, 0, 256])
        hist = cv.normalize(hist, hist).flatten()
        features.extend(hist)

        return features