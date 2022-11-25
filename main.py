import numpy

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
    for i in data:
        objectToClassify = i
        classOfObjectToClassify = int(objectToClassify[0])
        nearestNeighborDistance = numpy.inf
        nearestNeighborLocation = numpy.inf
        nearestNeighborLabel = numpy.inf
        for k in data:
            featuresToConsider = []
            featuresToConsider.append(objectToClassify[featureToAdd] - k[featureToAdd])
            for j in range(0, len(currentSet)):
                featuresToConsider.append(objectToClassify[currentSet[j]] - k[currentSet[j]])
            if k != i:
                distance = numpy.sqrt(sum(numpy.square(featuresToConsider)))
                if distance < nearestNeighborDistance:
                    nearestNeighborDistance = distance
                    nearestNeighborLocation = k
                    nearestNeighborLabel = int(nearestNeighborLocation[0])
        if classOfObjectToClassify == nearestNeighborLabel and nearestNeighborLabel != numpy.inf:
            correctClassifications += 1
    return correctClassifications / len(data)

def featureSearch(data):
    setOfFeatures = []
    # Forward Selection
    for i in range(1, len(data[0])):
        print("CURRENT SET OF FEATURES: ", setOfFeatures)
        print("At level ", i, " of the search tree.")
        bestSoFarAccuracy = 0
        for k in range(1, len(data[0])):
            accuracy = 0
            if k not in setOfFeatures:
                print("Considering adding option ", k)
                accuracy = kFoldCrossValidation(data, setOfFeatures, k)
                print("ACCURACY OF OPTION ", k, ": ", accuracy)
            if accuracy > bestSoFarAccuracy:
                bestSoFarAccuracy = accuracy
                featureToAdd = k
        setOfFeatures.append(featureToAdd)
        print("Added feature ", featureToAdd, "to set.")
    print("Final set of features: ", setOfFeatures)

def main():
    fileName = input("Enter a file name to read: ")
    data = readData(fileName)
    #if fileName == "":
    #    data = readData("CS170_Small_Data__24.txt")
    #else:
    #    data = readData("CS170_Large_Data__67.txt")
    print(len(data))
    featureSearch(data)

if __name__ == "__main__":
    main()