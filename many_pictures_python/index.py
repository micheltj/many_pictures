"""
This Program will slice an Input Image into x*y parts.
Each part will be replaced by an Image which will be extracted from a video.
We Replace the sliced parts based on the chi quadrat distance between an Image and the sliced part.
"""

import Descriptor
import Searcher
import target_image_manipulation
import cv2 as cv
import argparse
import csv

"""
Define the paths through console input to the directorys holding the required data and the paths who will receive the final image
dataset: path to mp4 file in the video folder
index: path there the csv file containing the average pixel value of the video frames will be stored
querry: path to the image which will be reconstructed with the images from the dataset
result_path: Where should the result Image be stored
index_cut: path there the csv file containing the average pixel values of the slices will be stored
Example Terminal Input : py many_pictures_python/index.py --dataset videos/test.mp4 --index index.csv --query bilder\main.png --result-path bilder\result.png --index_cut index_target.csv
"""
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
	help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-i", "--index", required = True,
	help = "Path to where the computed index will be stored")
ap.add_argument("-q", "--query", required = True,
	help = "Path to the query image")
ap.add_argument("-r", "--result-path", required = True,
	help = "Path to the result path")
ap.add_argument("-ii", "--index_cut", required = True,
	help = "Path to the cutted image index")
args = vars(ap.parse_args())

cd = Descriptor.Descriptor((8, 12, 3))

output = open(args["index"], "w")
"Load video and get the Frames per Second of the video"
video = cv.VideoCapture(args["dataset"])
fps = video.get(cv.CAP_PROP_FPS)

"""
minute: how much of the video do we use
id: counter for frames
shape: stores the shape of the frames (how many pixels in x and y direction)
size:
"""
minute = 1
id = 0
shape = 0
size = 100

"Look at each frame till video ends"
while(video.isOpened()):
    ret, frame = video.read()
    if ret == True:
        "put the bin combination for each frame in the matching csv"
        shape = frame.shape
        imageID = id
	    # describe the image
        features = cd.describe(frame)
	    # write the features to file
        features = [str(f) for f in features]
        output.write("%s,%s\n" % (imageID, ",".join(features)))
        id += 1
    else:
        break

"Cut the Input Image into mostly equal sized parts"
query = cv.imread(args["query"])
target_image = target_image_manipulation.image_manipulation(query, size)
target_image.cut(args)

with open(args["index_cut"]) as f:
    "Look for the corresponding frame for each Input Image part"
    searcher = Searcher.Searcher(args["index"])
    reader = csv.reader(f)
    for row in reader:
                features = [float(x) for x in row[1:]]
                (score, resultID) = searcher.search(features)[0]
                print(resultID)
                video.set(0, float(resultID))
                ret, frame = video.read()
                frame = cv.resize(frame, (size, size))
                "Put the output Image togehter"
                target_image.stich(frame, float(row[0])-1)
                
# close the index file
output.close()
target_image.print()