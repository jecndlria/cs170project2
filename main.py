import random

def readData(file):
    data = [] # 2D List that holds the entire dataset
    file = open(file, "r")
    for line in file:
        dataLine = [float(i) for i in line.split()]
        data.append(dataLine)
    file.close()
    return data

def kFoldCrossValidation(data, currentSet, featureToAdd):
    return random.random()

def featureSearch(data):
    setOfFeatures = []
    for i in range(1, len(data[0])):
        print("CURRENT SET OF FEATURES: ", setOfFeatures)
        print("At level ", i, " of the search tree.")
        bestSoFarAccuracy = 0
        for k in range(1, len(data[0])):
            accuracy = 0
            if k not in setOfFeatures:
                print("Considering adding option ", k)
                accuracy = kFoldCrossValidation(data, setOfFeatures, k)
            if accuracy > bestSoFarAccuracy:
                bestSoFarAccuracy = accuracy
                featureToAdd = k
        setOfFeatures.append(featureToAdd)
        print("Added feature ", featureToAdd, "to set.")
    print("Final set of features: ", setOfFeatures)

def main():
    fileName = input("Enter a file name to read: ")
    #data = readData(fileName)
    if fileName == "":
        data = readData("CS170_Small_Data__24.txt")
    else:
        data = readData("CS170_Large_Data__67.txt")
    print(len(data))
    featureSearch(data)

if __name__ == "__main__":
    main()