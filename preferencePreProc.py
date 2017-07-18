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

    for placeID in placesDict:
        #set food codes and prodcut codes variables
        currentPlace = placesDict[placeID]
        productType = currentPlace.productType
        if productType != -1:
            productType = productType.lower()
            productType = productType.strip()
            productCode = productCodesDict[productType]
            print(type(productCode))
            assert type(productCode) != list, "ProductCode is not int"
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
            assert type(foodCode) == int, "ProductCode is not int"
            setattr(currentPlace, "foodCode", foodCodeList)

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

def generate_place_matrices(cleanPlacesDict):
    finalMatrixDict = {}
    for placeID in cleanPlacesDict:
        place = cleanPlacesDict[placeID]
        if place.classCode == 1:
            columnList = ['productCode', 'foodCode', 'priceRange',
                          'water', 'soda', 'candy',
                          'reading', 'tech', 'takeout', 'bar', 'kids']
            finalMatrix = np.zeros( shape = (1,len(columnList)) )
            for i in range(len(columnList)):
                feature = getattr(place, columnList[i], 0)
                finalMatrix[0,i] = feature

            finalMatrixDict[placeID] = finalMatrix
    return finalMatrixDict
