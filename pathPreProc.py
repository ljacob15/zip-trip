#pathPreProc
import pandas as pd
from collections import OrderedDict
import pdb
import subprocess
import math


def generate_codes():
    '''
    Generates codes mapping food/product types in the airport to #s.
    '''
    #construct diciotnary mapping product types to productCodes
    productCodesDF = pd.read_excel('productCodes.xlsx', header = 0)
    productCodesDict = {}
    for i in range(productCodesDF.shape[0]):
        row = productCodesDF.iloc[i]
        productType = row.iloc[1].lower()
        productType = productType.strip()
        productCode = row.iloc[0]
        productCodesDict[productType] = productCode

    #construct diciotnary mapping food types to foodCodes
    foodCodesDF = pd.read_excel('foodCodes.xlsx', header = 0)
    foodCodesDict = {}
    for i in range(foodCodesDF.shape[0]):
        row = foodCodesDF.iloc[i]
        foodTypes = row.iloc[1]
        foodTypes = foodTypes.lower()
        foodTypeList = foodTypes.split(',')
        for foodType in foodTypeList:
            foodType = foodType.strip()
        foodTypeTuple = tuple(foodTypeList)
        foodCode = row.iloc[0]
        foodCodesDict[foodTypeTuple] = foodCode

    return productCodesDict, foodCodesDict


def clean_places(placesDict, productCodesDict, foodCodesDict):
    '''placesDict = raw dictionary of all Places
    productCodeDict = dict mapping product Type to product code
    foodCodeDict = dict mapping food Type to food code'''

    for placeID in placesDict:
        #set food codes and prodcut codes variables
        currentPlace = placesDict[placeID]
        #set product code
        setattr(currentPlace,"productCode", None)
        productType = currentPlace.productType
        if productType != -1:
            productType = productType.lower()
            productType = productType.strip()
            productCode = productCodesDict[productType]
#            assert type(productCode) == int, "productCode is not int"
            setattr(currentPlace, "productCode", productCode)

        #set list of foodCodes
        setattr(currentPlace,"foodCodes", None)
        if currentPlace.foodType != -1:
            foodCodeList = []
            foodTypes = currentPlace.foodType.lower()
            foodTypeList = foodTypes.split(',')
            cleanFoodTypeList = []
            for foodType in foodTypeList:
                cleanFoodTypeList.append(foodType.strip())
            for foodTypeTuple in foodCodesDict:
                for foodType in cleanFoodTypeList:
                    if foodType in foodTypeTuple:
                        foodCodeList.append(foodCodesDict[foodTypeTuple])

            #eliminate duplicates
            Set = set(foodCodeList)
            foodCodeList = list(Set)
            if len(foodCodeList) > 0:
                foodCodes = foodCodeList
            setattr(currentPlace, "foodCodes", foodCodes)

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

        #set terminal codes (D = 0, E = 1)
        if currentPlace.terminal not in ['D', 'E']:
            currentPlace.terminal = -1
        else:
            terminalCodes = {"D": 0, "E": 1}
            currentPlace.terminal = terminalCodes[currentPlace.terminal]

        #clean up nearestGate column
        if type(currentPlace.nearestGate) != None and currentPlace.nearestGate != -1:
            currentPlace.nearestGate = currentPlace.nearestGate.strip()
            currentPlace.nearestGate = int(currentPlace.nearestGate[1:])

    # import pdb; pdb.set_trace()
    return placesDict

def get_places(cleanPlacesDict, c1Categs, c2Categs,
               terminal, location, timeLeft,
               currentTimeOG, userFoodCodes):
    '''cleanPlacesDict = dictionary mapping ids to places in the airport
    all place attributes are clean, numerical codes
    c1Categs = ranked list of categories that user is predicted to prefer
    (same for c2Categs)
    terminal = 0 for terminal D, 1 for terminal E
    timeLeft = integer value, time remaining in minutes
    operation: narrows categories based on time left,
    gets only open places for each cateogry'''
    #narrow down the category lists based on the timeLeft
    timesLeft = [240, 180, 120, 90, 60, 45, 30, 20]
    c1Nums =    [4, 3, 3, 2, 2, 1, 1, 0]
    c2Nums =    [5, 4, 3, 3, 2, 2, 1, 1]
    c1Num = 6
    c2Num = 7
    for i in range(len(timesLeft)):
        if timeLeft <= timesLeft[i]:
            c1Num = c1Nums[i]
            c2Num = c2Nums[i]
    c1NarrowedCategs = c1Categs[:c1Num]
    c2NarrowedCategs = c2Categs[:c2Num]

    subprocess.run("echo Robert's narrowed categories based on time:")
    subprocess.run('cat', input = str(c1NarrowedCategs), universal_newlines = True)
    subprocess.run('cat', input = str(c2NarrowedCategs), universal_newlines = True)
    subprocess.run('echo')
    #now we have narrowed category lists that the user has time for (estimated)
    #next, find all places (in the relevant terminal) in those categories

    #Dictionary ensures we keep the category by category information
    #Ordered Dict ensures the categories are still ranked
    class1CPMap = OrderedDict()
    class2CPMap = OrderedDict()

    #get only open places for each of the narrowed categories
    for category in c1NarrowedCategs:
        class1CPMap[category] = []
        for placeID in cleanPlacesDict:
            place = cleanPlacesDict[placeID]
            openTag = False
            currentHour = currentTimeOG.hour
            currentMinute = currentTimeOG.minute
            currentTime = currentHour*100+ currentMinute
            # pdb.set_trace()
            if len (place.hoursList) == 2:
                if  int(place.hoursList[0]) < currentTime < int(place.hoursList[1])-15:
                    openTag = True
            if len (place.hoursList) > 2:
                if  int(place.hoursList[0]) < currentTime < int(place.hoursList[1])-15:
                    openTag = True
                if  int(place.hoursList[2]) < currentTime < int(place.hoursList[3])-15:
                    openTag = True
            if place.categoryCode == category and place.terminal == terminal and openTag == True:
                class1CPMap[category].append(place)

    for category in c2NarrowedCategs:
        class2CPMap[category] = []
        for placeID in cleanPlacesDict:
            place = cleanPlacesDict[placeID]
            if place.categoryCode == category and place.terminal == terminal: #and openTag == True:
                class2CPMap[category].append(place)

    if userFoodCodes:
        #if the user has food preferences, UPDATE the path to return only places of those preferences
        # for category in class1CPMap:
        #     placeList = class1CPMap[category]
        #     for place in placeList:
        #         if place.foodCode and place.foodCode not in userFoodCodes:
        #                 placeList.remove(place)

        #if user has food preferences, DISPLAY those preferences in addition to the current path
        preferredPlaceList = []
        for placeID in cleanPlacesDict:
            place = cleanPlacesDict[placeID]
            if place.foodCodes:
                for foodCode in place.foodCodes:
                    if foodCode in userFoodCodes and (math.fabs(place.nearestGate - location) <= 5):
                        preferredPlaceList.append(place)
                        break
        '''ideally return only open preferred places, but that's not implemented yet'''
        return class1CPMap, class2CPMap, preferredPlaceList

    # import pdb; pdb.set_trace()

    return class1CPMap, class2CPMap, None



'''
def generate_fake_categories():
    c1Categs = [2, 3, 4, 6, 7, 21]
    c2Categs = [5, 8, 9, 10, 11, 12, 13, 18, 19]
    timesLeft = [240, 180, 120, 90, 60, 45, 30]
    c1Nums =    [6, 5, 4, 3, 2, 1, 1]
    c2Nums =    [6, 5, 4, 3, 2, 2, 1]
    randomIndex = rand.randint(0,6)
    #based on the timetoBoard, choose x Class 1 and y Class2
    #categories to feed into phase 2
    timeLeft = timesLeft[randomIndex]
    c1Num = c1Nums[randomIndex]
    c2Num = c2Nums[randomIndex]
    c1FinalCategs = []
    c2FinalCategs = []
    #resemble output of the machine
    #list of class 1 and class 2 categories the user will prefer
    c1FinalCategs = rand.sample(c1Categs, c1Num)
    c2FinalCategs = rand.sample(c2Categs, c2Num)
    print(timeLeft)
    print(c1Num)
    print(c2Num)
    print(c1FinalCategs)
    print(c2FinalCategs)
    return c1FinalCategs, c2FinalCategs, timeLeft
'''
