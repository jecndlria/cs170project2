data = [[]]

def readData(file):
    file = open(file, "r")
    for line in file:
        dataLine = [float(i) for i in file.readline().split()]
        data.append(dataLine)
    file.close()

def main():
    fileName = input("Enter a file name to read: ")
    #readData(fileName)
    readData("CS170_Large_Data__67.txt")
    print(data)

if __name__ == "__main__":
    main()