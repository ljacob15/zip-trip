import extractor
import preferencePreProc
import preferenceEngine
import preferencePostProc
from decorators import timer

from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np

def generate_recommendations():

    userTrainDF = extractor.extract_users(filer = 'userTrainData.xlsx')
    # print("Training set constructed")
    # proc = subprocess.run("echo Training set constructed")

    userTestDF = extractor.extract_users(filer = 'userTestData.xlsx')
    # print("Testing set constructed")
    # subprocess.run("echo Testing set constructed")

    userTrainMatrix, labels = preferencePreProc.clean_users(userTrainDF)
    userTestMatrix = preferencePreProc.clean_users(userTestDF)
    # print("Training and testing sets cleaned")
    # subprocess.run("echo Training and testing sets cleaned")

    #return userTrainMatrix, labels, userTestMatrix
    df,time = bring_forth_300(userTrainMatrix, labels,
                                                 userTestMatrix)

    df.to_csv('data/300Results.csv', header = True)
    print('Time Taken: ' + str(round(time,2)))
    return None



@timer
def bring_forth_300(trainMatrix, labels, testMatrix,):

    the300 = np.empty((300,5),dtype = float)
    clf = KNeighborsClassifier(n_neighbors = 10, weights = 'distance')
    clf.fit(trainMatrix, labels)

    for row in range(the300.shape[0]):
        bobData = testMatrix[row]
        bobData = bobData.reshape(1,-1)
        predictions = clf.predict_proba(bobData)
        the300[row,:] = predictions

    df = pd.DataFrame(the300, columns = ["Business", 'Frugal Spender',
                                         'Medium Spender', "Medium High Spender",
                                         'High Spender'])

    return df

generate_recommendations()
