import things

import pandas as pd
import numpy as np
import pdb


def clean_users(inputDF):
    '''inputDF = dataframe of user flight data to clean'''
    userDF = inputDF.copy()

    #gender codes: male, female, or unspecified
    genderCodes = {"F": 0, "M":1, "O":2}
    #type codes: business or leisure
    typeCodes = {"B":0, "L":1}
    #cabinPreference codes
    cabinPreferenceCodes = {"B": 0, "F":1, "Q":2, "Y":3}
    #userType codes
    userTypeCodes = {"Business": 1, "Frugal Spender": 2,
                     "Medium Spender": 3, "Medium High Spender": 4,
                     "High Spender":5}

    for i in userDF.index:
        userDF.loc[i,'gender'] = genderCodes[userDF.loc[i,'gender']]
        userDF.loc[i,'type'] = typeCodes[userDF.loc[i,'type']]
        userDF.loc[i,'cabinPreference'] = cabinPreferenceCodes[userDF.loc[i,'cabinPreference']]
        userClassList = None
        #if the data is training data:
        if "userType" in userDF.columns:
            userDF.loc[i,'userType'] = userTypeCodes[userDF.loc[i,'userType']]

    #if it's the training set, return matrix and labels. If not, just return matrix.
    if 'userType' in userDF.columns:
        #extract the column with the labels
        userClassList = userDF.loc[:,'userType']
        userClassList = list(userClassList)
        #drop the user class labels from the training set
        userDF = userDF.drop(labels = "userType", axis = 1)
        finalMatrix = np.array(userDF)
        return finalMatrix, userClassList

    finalMatrix = np.array(userDF)
    return finalMatrix

'''
def generate_place_matrices(cleanPlacesDict):
    finalMatrixDict = {}
    for placeID in cleanPlacesDict:
        place = cleanPlacesDict[placeID]
        if place.classCode == 1:
            columnList = ['priceRange',
                          'water', 'soda', 'candy',
                          'reading', 'tech', 'takeout', 'bar', 'kids']
            finalMatrix = np.zeros( shape = (1,len(columnList)) )
            for i in range(len(columnList)):
                feature = getattr(place, columnList[i], 0)
                finalMatrix[0,i] = feature

            finalMatrixDict[placeID] = finalMatrix
    return finalMatrixDict
'''
