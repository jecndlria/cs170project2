import numpy

def readData(file):
    data = [] # 2D List that holds the entire dataset
    file = open(file, "r")
    for line in file:
        dataLine = [float(i) for i in line.split()]
        data.append(dataLine)
    file.close()
    return data

def kCrossValidation(data, currentSet, featureToAdd):
    accuracy = 0.5
    return accuracy

def featureSearch(data):
    setOfFeatures = []
    for i in range(1, len(data[0])):
        print("At level ", i, " of the search tree.")
        for k in range(1, len(data[0])):
            if k not in setOfFeatures:
                print("Considering adding option ", k)


def main():
    fileName = input("Enter a file name to read: ")
    #readData(fileName)
    data = readData("CS170_Small_Data__24.txt")
    #data = readData("CS170_Large_Data__67.txt")
    for i in data:
        print(i)
    print(len(data))
    featureSearch(data)

if __name__ == "__main__":
    main()