import pandas as pd
import numpy
import things
import pdb

def extract_places(filer = 'placeAttributes.xlsx'):
    '''
    Gets place data from specified file
    Returns: placesDict: Dictionary mapping place ID to Place object.
    Place object contains all attributes of the given place.
    '''

    placesDict = {}
    dataFrame = pd.read_excel(filer, header = 0, index_col = 0 )

    #list of titles for each place attribute
    columnsList = list(dataFrame.columns.values)

    #iterate through each row, constructing the place object and adding to dict
    for row in range(dataFrame.shape[0]):
        #extract the place
        currentPlace = dataFrame.iloc[row]
        #construct diciontary of placeAttributes to feed into object constructor
        attributeDict = {}
        for i in range(currentPlace.shape[0]):
            columnName = columnsList[i]
            columnValue = currentPlace.loc[columnName]
            attributeDict[columnName] = columnValue
        #construct the Place object
        placeObject = things.Place(attributeDict = attributeDict)
        #add thr new place object to placesDict
        idNum = placeObject.get_id()
        placesDict[idNum] = placeObject

    return placesDict

def extract_users(filer = 'userTrainData.xlsx'):
    #get user info from csv
    dataFrame = pd.read_excel(filer, header = 0, index_col = 0 )
    return dataFrame
