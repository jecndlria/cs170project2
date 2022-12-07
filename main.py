import numpy
from copy import deepcopy
import sys
from datetime import datetime
import time

def readData(file):
    data = [] # 2D List that holds the entire dataset
    file = open(file, "r")
    for line in file:
        dataLine = [float(i) for i in line.split()]
        data.append(dataLine)
    file.close()
    return data

def kFoldCrossValidation(data, currentSet, featureToAdd):
    correctClassifications = 0
    if not currentSet and featureToAdd == 0: return 0.5
    for i in data:
        objectToClassify = i
        classOfObjectToClassify = int(objectToClassify[0])
        nearestNeighborDistance = numpy.inf
        nearestNeighborLocation = numpy.inf
        nearestNeighborLabel = numpy.inf
        for k in data:
            featuresToConsider = []
            if featureToAdd != 0:
                featuresToConsider.append(objectToClassify[featureToAdd] - k[featureToAdd])
            for j in range(0, len(currentSet)):
                featuresToConsider.append(objectToClassify[currentSet[j]] - k[currentSet[j]])
            if k != i and featuresToConsider:
                featuresToConsider = numpy.square(featuresToConsider)
                distance = numpy.sqrt(sum(featuresToConsider))
                if distance < nearestNeighborDistance:
                    nearestNeighborDistance = distance
                    nearestNeighborLocation = k
                    nearestNeighborLabel = int(nearestNeighborLocation[0])
        if classOfObjectToClassify == nearestNeighborLabel and nearestNeighborLabel != numpy.inf:
            correctClassifications += 1
    return correctClassifications / len(data)

def featureSearch(data, algorithm):
    setOfFeatures = []
    optimalFeatureSet = []
    optimalAccuracy = 0
    lastSeenAccuracy = 0
    # Forward Selection
    if algorithm == 1:
        for i in range(1, len(data[0])):
            print("CURRENT SET OF FEATURES:", setOfFeatures)
            print("At level", i, "of the search tree.")
            bestSoFarAccuracy = 0
            for k in range(1, len(data[0])):
                accuracy = 0
                if k not in setOfFeatures:
                    accuracy = kFoldCrossValidation(data, setOfFeatures, k)
                    print("ACCURACY OF FEATURES", setOfFeatures, "with", k, "added:", accuracy)
                if accuracy > bestSoFarAccuracy:
                    bestSoFarAccuracy = accuracy
                    featureToAdd = k
            setOfFeatures.append(featureToAdd)
            print("Added feature", featureToAdd, "to set, giving us an accuracy of", bestSoFarAccuracy, '\n')
            if bestSoFarAccuracy > optimalAccuracy:
                optimalAccuracy = bestSoFarAccuracy
                optimalFeatureSet = deepcopy(setOfFeatures)
            if lastSeenAccuracy > bestSoFarAccuracy:
                print("WARNING: Accuracy has decreased, but the search will continue!\n")
            lastSeenAccuracy = bestSoFarAccuracy
    # Backward Elimination
    if algorithm == 2:
        for i in range(1, len(data[0])):
            setOfFeatures.append(i)
        for i in range(1, len(data[0])):
            print("CURRENT SET OF FEATURES:", setOfFeatures)
            print("At level", i, "of the search tree.")
            bestSoFarAccuracy = 0
            featureToRemove = 0
            for k in setOfFeatures:
                backwardEliminationTest = deepcopy(setOfFeatures)
                backwardEliminationTest.remove(k)
                accuracy = kFoldCrossValidation(data, backwardEliminationTest, 0)
                print("ACCURACY OF FEATURES", backwardEliminationTest, "eliminating", k ,": ", accuracy)
                if accuracy > bestSoFarAccuracy:
                    bestSoFarAccuracy = accuracy
                    featureToRemove = k
            if setOfFeatures: setOfFeatures.remove(featureToRemove)
            print("Removed feature", featureToRemove, "from set, giving us an accuracy of", bestSoFarAccuracy, '\n')
            if bestSoFarAccuracy > optimalAccuracy:
                optimalAccuracy = bestSoFarAccuracy
                optimalFeatureSet = deepcopy(setOfFeatures)
            if lastSeenAccuracy > bestSoFarAccuracy:
                print("WARNING: Accuracy has decreased, but the search will continue!\n")
            lastSeenAccuracy = bestSoFarAccuracy
    return (optimalAccuracy, optimalFeatureSet)

def main():
    startTime = time.process_time()
    timestamp = str(datetime.now())
    fileName = input("Enter a file name to read: ")
    sys.stdout=open(f"outputlogs/{fileName} at {timestamp}.txt", "w")
    algorithm = input("Enter 1 to use Forward Selection, or 2 to use Backward Elimination: ")
    data = readData(fileName)
    print("This dataset has", len(data[0]) - 1, "features and", len(data), "instances.\n")
    answer = featureSearch(data, int(algorithm))
    print("FINISH: Optimal set of features is", answer[1], ", with an accuracy of ", answer[0])
    sys.stdout.close()
    totalTime = time.process_time() - startTime
    print("Time to compute: ", round(totalTime, 2))

if __name__ == "__main__":
    main()