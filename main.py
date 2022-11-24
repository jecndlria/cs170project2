data = [[]] # 2D List that holds the entire dataset

def readData(file):
    file = open(file, "r")
    for line in file:
        dataLine = [float(i) for i in file.readline().split()]
        data.append(dataLine)
    file.close()

def kCrossValidation(data, currentSet, featureToAdd):
    accuracy = 0.5
    return accuracy

def featureSearch(data):
    setOfFeatures = []


def main():
    fileName = input("Enter a file name to read: ")
    #readData(fileName)
    readData("CS170_Large_Data__67.txt")
    print(data)

if __name__ == "__main__":
    main()