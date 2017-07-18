import things

import pandas as pd
import numpy as np

def generate_codes():
    #construct diciotnary mapping product types to productCodes
    productCodesDF = pd.read_excel('productCodes.xlsx', header = 0)
    productCodesDict = {}
    for i in range(productCodesDF.shape[0]):
        row = productCodesDF.iloc[i]
        key = row.iloc[1].lower()
        key = key.strip()
        value = row.iloc[0]
        productCodesDict[key] = value

    #construct diciotnary mapping product types to productCodes
    foodCodesDF = pd.read_excel('foodCodes.xlsx', header = 0)
    foodCodesDict = {}
    for i in range(foodCodesDF.shape[0]):
        row = foodCodesDF.iloc[i]
        key = row.iloc[1]
        value = row.iloc[0]
        foodCodesDict[key] = value
    return productCodesDict, foodCodesDict



def clean_places(placesDict, productCodesDict, foodCodesDict):
    '''placesDict = raw dictionary of all Places
    productCodeDict = dict mapping product Type to product code
    foodCodeDict = dict mapping food Type to food code'''
    for placeID in placesDict:
        #set food codes and prodcut codes variables
        currentPlace = placesDict[placeID]
        productType = currentPlace.productType
        if productType != -1:
            productType = productType.lower()
            productType = productType.strip()
            productCode = productCodesDict[productType]
#            assert type(productCode) == int, "productCode is not int"
            setattr(currentPlace, "productCode", productCode)
        if currentPlace.foodType != -1:
            foodCodeList = []
            foodTypeList = currentPlace.foodType.split(",")
            for item in foodCodesDict:
                for foodType in foodTypeList:
                    if foodType in item:
                        foodCodeList.append(foodCodesDict[item])
            Set = set(foodCodeList)
            foodCodeList = list(Set)
            foodCode = -1
            if len(foodCodeList) > 0:
                foodCode = foodCodeList[0]
#            assert type(foodCode) == int, "foodCode is not int"
            setattr(currentPlace, "foodCode", foodCode)

        #set variables for opening hour and closing hours
        hours = currentPlace.openHours
        openIntervalsList = hours.split(",")
        hoursList = []
        for hours in openIntervalsList:
            singleHours = hours.split("-")
            for hour in singleHours:
                hour = hour.strip()
                hour = hour.replace(":", "")
                hoursList.append(hour)
#        import pdb; pdb.set_trace()
        setattr(currentPlace, "hoursList", hoursList)
    return placesDict

    #set terminal codes (D = 0, E = 1)
    if self.terminal != ("D" or "E"):
        self.terminal = -1
    else:
        terminalCodes = {"D": 0, "E": 1}
        self.terminal = terminalCodes[self.terminal]
        
    #clean up nearestGate column
    if type(self.nearestGate) != None and self.nearestGate != -1:
        self.nearestGate.strip()
        self.nearestGate = int(self.nearestGate[1:])


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

