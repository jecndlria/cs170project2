import numpy
from copy import deepcopy
import sys
from datetime import datetime
import time

# This function takes the .txt dataset as input, and returns it as a 2D list such that:
# Each row is an object, and each column is a feature (the first being the object's class).
def readData(file):
    data = [] # 2D List that holds the entire dataset
    file = open(file, "r")
    for line in file:
        # Split each line in the dataset into a list. Append that list to the list of lists.
        dataLine = [float(i) for i in line.split()]
        data.append(dataLine)
    file.close()
    return data

# Leave-one-out cross validation using Nearest Neighbor Classifier
    # Given a full dataset, a set of features, and (if using forward selection) a feature to add to that set, use the nearest neighbor algorithm to test that set of features:
    # For each object in the dataset, we will attempt to classify it using it's nearest neighbor relative to the features we want to test.
    # Returns the accuracy of the current set of features (+ the feature being added to that set)
# data == the entire dataset 
# currentSet == the current set of features we are using
# featureToAdd == the feature we are considering adding to the currentSet
# NOTE: If featureToAdd == 0, then only the accuracy of the currentSet is considered. 
def kFoldCrossValidation(data, currentSet, featureToAdd):
    correctClassifications = 0
    if not currentSet and featureToAdd == 0: return 0.5     # If we are taking no features into account, then we have a 50% to correctly classify the object (since there are 2 classes) 
    for i in data:
        objectToClassify = i                                # Object we are classifying 
        classOfObjectToClassify = int(objectToClassify[0])  # Actual class of object to classify
        nearestNeighborDistance = numpy.inf                 # Distance to closest neighbor (initialized to infinity)
        nearestNeighborLocation = numpy.inf                 # Index of the object in the dataset
        nearestNeighborLabel = numpy.inf                    # Class of the nearest neighbor of object in question
        for k in data:
            featuresToConsider = []                         # List of the values of the features we are going to consider.
            if featureToAdd != 0:                           # If we don't want to add a feature, then we simply calculate the accuracy of currentSet
                featuresToConsider.append(objectToClassify[featureToAdd] - k[featureToAdd])     # We append the difference between the features we want to consider to featuresToConsider (if it is not 0, since k[0] is the class, not a feature)
            for j in range(0, len(currentSet)):
                featuresToConsider.append(objectToClassify[currentSet[j]] - k[currentSet[j]])   # Append the distance between each feature in currentSet of objectToClassify and the current object
            if k != i and featuresToConsider:                                                   # (k != i) -> Don't self compare. (featuresToConsider) -> only do this if the list isn't empty
                featuresToConsider = numpy.square(featuresToConsider)                           # Square the distance between each feature.
                distance = numpy.sqrt(sum(featuresToConsider))                                  # Sum up the distances between each feature, and square root it (Euclidean Distance between two objects)
                if distance < nearestNeighborDistance:                                          # If this is the shortest distance seen so far, it is the nearest neighbor so far.
                    nearestNeighborDistance = distance                                              # So, save it's distance, location, and class label.
                    nearestNeighborLocation = k
                    nearestNeighborLabel = int(nearestNeighborLocation[0])
        if classOfObjectToClassify == nearestNeighborLabel and nearestNeighborLabel != numpy.inf:   # After we have compared the current objectToClassify with every other object in the dataset, determine if it was correctly classified by comparing the actual class label with it's nearest neighbor's label.
            correctClassifications += 1                                                             # If they're the same, it's correct!
    return correctClassifications / len(data)                                                       # Accuracy of currentSet + featureToAdd = # of correct classificatoins / size of dataset

def featureSearch(data, algorithm):
    setOfFeatures = []     # Keeps track of current set being considered.
    optimalFeatureSet = []  # Keeps track of best feature set so far.
    optimalAccuracy = 0    # Keeps track of best accuracy seen so far.
    lastSeenAccuracy = 0  # Best accuracy of the previous level of the search tree (used to determine if accuracy went down)
    
    # Forward Selection
        # Start with an empty set of features.
        # Test each feature we haven't added to the set of features using k-fold cross validation.
        # The feature whose addition results in the highest accuracy will be added to the current set of features (greedy selection).
        # We return the set of features who had the highest accuracy.
    if algorithm == 1:
        for i in range(1, len(data[0])):
            print("CURRENT SET OF FEATURES:", setOfFeatures)
            print("At level", i, "of the search tree.")
            bestSoFarAccuracy = 0            # Keeps track of the best accuracy seen during one level of the search.
            for k in range(1, len(data[0])):
                accuracy = 0                 # Keeps track of the accuracy of the set of features, plus the feature we are considering adding.
                if k not in setOfFeatures:   # Only consider a feature if it isn't already in the setOfFeatures
                    accuracy = kFoldCrossValidation(data, setOfFeatures, k)   # Use leave one out validation to get accuracy of current setOfFeatures, plus the current feature we are considering
                    print("ACCURACY OF FEATURES", setOfFeatures, "with", k, "added:", accuracy)
                if accuracy > bestSoFarAccuracy: # Update the bestSoFaraccuracy if it is beaten by previous calculation  
                    bestSoFarAccuracy = accuracy
                    featureToAdd = k
            setOfFeatures.append(featureToAdd)   # Add the feature that had the highest accuracy with the current setOfFeatures to the setOfFeatures.
            print("Added feature", featureToAdd, "to set, giving us an accuracy of", bestSoFarAccuracy, '\n')
            if bestSoFarAccuracy > optimalAccuracy:     # Update the optimalAccuracy if adding the feature increased the accuracy of the setOfFeatures
                optimalAccuracy = bestSoFarAccuracy
                optimalFeatureSet = deepcopy(setOfFeatures) # Note that this must be a deep copy, otherwise the optimalFeatureSet would just point to setOfFeatures.
            if lastSeenAccuracy > bestSoFarAccuracy:        # If adding the feature brought the accuracy down, let the user know.
                print("WARNING: Accuracy has decreased, but the search will continue!\n")
            lastSeenAccuracy = bestSoFarAccuracy

    # Backward Elimination
        # How does this work? Unlike forward elimination, backward elimination starts with a FULL set of features.
        # We test each feature by removing it from the set of features, and calculate its accuracy by running k-fold cross validation.
        # The feature whose removal results in the highest accuracy at that level of the search tree will be removed, until there are no features left in the set of features.
        # We return the set of features who had the highest accuracy.
        # Backward elimination and forward selection will not necessarily give you the same answer.
    # NOTE: There is likely a more elegant way to implement this rather than copy pasting and rewriting the algorithm.
    # However, this was the method that made the most sense to me, and was the fastest to implement.
    if algorithm == 2:
        for i in range(1, len(data[0])): # Add every feature to the setOfFeatures, since backward elimination starts with a complete set of features.
            setOfFeatures.append(i)
        for i in range(1, len(data[0])):
            print("CURRENT SET OF FEATURES:", setOfFeatures)
            print("At level", i, "of the search tree.")
            bestSoFarAccuracy = 0   # Keeps track of the best accuracy seen during one level of the search.
            featureToRemove = 0     # Keeps track of the feature whose removal results in the highest accuracy. 
            for k in setOfFeatures:                                 # NOTE: We iterate through the current set of features.
                backwardEliminationTest = deepcopy(setOfFeatures)   # Copy the current set of features
                backwardEliminationTest.remove(k)                   # Remove the current feature, and test the accuracy of that set of features.
                accuracy = kFoldCrossValidation(data, backwardEliminationTest, 0)
                print("ACCURACY OF FEATURES", backwardEliminationTest, "eliminating", k ,": ", accuracy)
                if accuracy > bestSoFarAccuracy:                    # Take the best accuracy seen, and remove the feature whose removal gave us the highest accuracy.
                    bestSoFarAccuracy = accuracy
                    featureToRemove = k
            if setOfFeatures: setOfFeatures.remove(featureToRemove) # The set of features will be empty at the end, so don't do this line if it is empty as it will crash the program.
            print("Removed feature", featureToRemove, "from set, giving us an accuracy of", bestSoFarAccuracy, '\n')
            if bestSoFarAccuracy > optimalAccuracy:        # Update the optimalAccuracy if removing the feature increased the accuracy of the setOfFeatures
                optimalAccuracy = bestSoFarAccuracy
                optimalFeatureSet = deepcopy(setOfFeatures)
            if lastSeenAccuracy > bestSoFarAccuracy:    # If adding the feature brought the accuracy down, let the user know
                print("WARNING: Accuracy has decreased, but the search will continue!\n")
            lastSeenAccuracy = bestSoFarAccuracy
    return (optimalAccuracy, optimalFeatureSet)   # Return optimal accuracy and feature set as a tuple.

def main():
    startTime = time.process_time()                                                                 # Start timer
    timestamp = str(datetime.now())                                                                 # Timestamp for traceback logs to prevent overwriting 
    fileName = input("Enter a file name to read: ")
    sys.stdout=open(f"outputlogs/{fileName} at {timestamp}.txt", "w")                               # Create file for traceback log
    algorithm = input("Enter 1 to use Forward Selection, or 2 to use Backward Elimination: \n")
    data = readData(fileName)
    print("This dataset has", len(data[0]) - 1, "features and", len(data), "instances.\n")          # len(data[0]) - 1, since we don't count the classification.
    answer = featureSearch(data, int(algorithm))                                                    # Run feature search and k-fold cross validation on the dataset              
    print("FINISH: Optimal set of features is", answer[1], ", with an accuracy of ", answer[0])
    totalTime = time.process_time() - startTime                                                     # Calculate time taken
    print("Time to compute:", round(totalTime, 1), " seconds.")
    sys.stdout.close()                                                                              # Close traceback log to save.

if __name__ == "__main__":
    main()