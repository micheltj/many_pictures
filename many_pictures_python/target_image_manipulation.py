"""
This class will cut the Input Image in x*y big parts.
Furtheremore this class also stiches the replaced parts back to gather to create an output image"
"""
import Descriptor
import numpy as np
import cv2 as cv

class image_manipulation():
    def __init__(self, image, size):
        """
        image: Input Image
        cropped_image:
        divider: step size (the sliced parts will usualy be squares with x = y = divider exeptions can occure near the edges)
        size: size of the images replacing the Input Image parts
        final_image: definition of the size of the final image which will be a multiple of size
        """
        self.image = image
        self.cropped_image = []
        self.divider = 10
        self.size = size
        self.final_image = np.zeros((self.size*int(np.floor(self.image.shape[0]/self.divider)+1), self.size*int(np.floor(self.image.shape[1]/self.divider)+1), 3))
        
    
    def cut(self, dir):
        "Get the bin combination for the Input Image"
        cd = Descriptor.Descriptor((8, 12, 3))
        output = open(dir["index_cut"], "w")
        self.imageID = 1
        """
        Cut the Image
        """
        for i in range(0, self.image.shape[0], self.divider):
            for j in range(0, self.image.shape[1], self.divider):
                if (j + self.divider > self.image.shape[1] and i + self.divider < self.image.shape[0]):

                    self.cropped_image = self.image[i : i + self.divider,j: self.image.shape[1]]
                    features = cd.describe(self.cropped_image)
	                # write the features to file
                    features = [str(f) for f in features]
                    output.write("%s,%s\n" % (self.imageID, ",".join(features)))

                elif (j + self.divider < self.image.shape[1] and i + self.divider < self.image.shape[0]):

                    self.cropped_image = self.image[i : i + self.divider,j: j + self.divider]
                    features = cd.describe(self.cropped_image)
	                # write the features to file
                    features = [str(f) for f in features]
                    output.write("%s,%s\n" % (self.imageID, ",".join(features)))

                elif (j + self.divider > self.image.shape[1] and i + self.divider > self.image.shape[0]):

                    self.cropped_image = self.image[i : self.image.shape[0],j : self.image.shape[1]]
                    features = cd.describe(self.cropped_image)
	                # write the features to file
                    features = [str(f) for f in features]
                    output.write("%s,%s\n" % (self.imageID, ",".join(features)))

                elif (j + self.divider < self.image.shape[1] and i + self.divider > self.image.shape[0]):

                    self.cropped_image = self.image[i : self.image.shape[0],j : j + self.divider]
                    features = cd.describe(self.cropped_image)
	                # write the features to file
                    features = [str(f) for f in features]
                    output.write("%s,%s\n" % (self.imageID, ",".join(features)))

                self.imageID += 1
                
    
    def stich(self, frame, id):
        "Replace the Input Image parts with the corresponding video frame"

        if id < (np.floor(self.image.shape[1]/self.divider)):
            x = 0
            y = (id-(np.floor(id/(np.floor(self.image.shape[1]/self.divider)+1))))*self.size
        else:
            x = (np.floor(id/(np.floor(self.image.shape[1]/self.divider)+1)))*self.size
            y = (id-(np.floor(id/(np.floor(self.image.shape[1]/self.divider)+1))*(np.floor(self.image.shape[1]/self.divider)+1)))*self.size
        
        self.final_image[int(x) : int(x) + self.size,int(y) : int(y) + self.size] = frame

    def print(self):
        cv.imwrite("bilder/result.png", self.final_image)
