from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd
import pdb


def predict_user_type(trainMatrix, labels, testMatrix,):
    '''
    Trains and tests KNN algorithm
    '''

    #train machine
    clf = KNeighborsClassifier(n_neighbors = 10, weights = 'distance')
    clf.fit(trainMatrix, labels)

    #grab Robert's userFlightData from the testing dataset
    bob = testMatrix[3]
    bob = bob.reshape(1,-1)

    #test machine
    predictions = clf.predict_proba(bob)
    predictions = predictions.reshape(-1)
    predictions = predictions.tolist()

    
    return predictions
