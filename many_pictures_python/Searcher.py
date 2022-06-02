import numpy as np
import csv

"""
Will look for the same bin Combination in the index.csv.
If one or more matching bin combinations are found look for the frame with the smallest chi2 distance
"""

class Searcher:
    def __init__(self, indexPath):
		# store our index path
        self.indexPath = indexPath
    def search(self, queryFeatures, limit = 1):
		# initialize our dictionary of results
        results = {}
        
        with open(self.indexPath) as f:
            reader = csv.reader(f)

            for row in reader:
                features = [float(x) for x in row[1:]]
                d = self.chi2_distance(features, queryFeatures)

                results[row[0]] = d

            f.close()

        results = sorted([(v, k) for (k, v) in results.items()])
        return results[:limit]

    def chi2_distance(self, histA, histB, eps = 1e-10):
	# compute the chi-squared distance
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
            for (a, b) in zip(histA, histB)])
	# return the chi-squared distance
        return d

