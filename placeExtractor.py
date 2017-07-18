import pandas as pd
import numpy
import things

def extract_places():
    #this list will store the places, indexed by their placeID's.
    placesDict = {}
    dataFrame = pd.read_excel('placeAttributes.xlsx', header = 0, index_col = 0 )
    #iterate through each row, constructing the place object and adding to dict

    columnsList = list(dataFrame.columns.values)
    for row in range(dataFrame.shape[0]):
        #extract the place
        currentPlace = dataFrame.iloc[row]
        attributeDict = {}
        #construct diciontary of placeAttributes to feed into object constructor
#        import pdb; pdb.set_trace()
        for i in range(currentPlace.shape[0]):
            columnName = columnsList[i]
            columnValue = currentPlace.loc[columnName]
            attributeDict[columnName] = columnValue
        #construct the Place
        placeObject = things.Place(attributeDict = attributeDict)
        idNum = placeObject.get_id()
        #add new Place to dictionary
        placesDict[idNum] = placeObject

    return placesDict




'''
id = place.loc("id"),
name = place.loc("name"),
terminal = place.loc("terminal"),
className = place.lod("class"),
cateory = place.loc("category")
'''
