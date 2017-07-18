import random as rand
import numpy as np
import math



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
        
def find_path(cleanPlacesDict, c1Categs, c2Categs, terminal, gate, timeLeft):
    #generate dict of Class 1 places that are from a 
    #category in the c1Categs list
    c1cxPlaces = {}
    #same for Class 2 places that are from a category in c2Categs
    c2cyPlaces = {}
    for placeID in cleanPlacesDict:
        place = cleanPlacesDict[placeID]
        if place.categoryCode in c1Categs:
            c1cxPlaces[placeID] = place
        if place.categoryCode in c1Categs:
            c2cyPlaces[placeID] = place
    return c1cxPlaces, c2cyPlaces

#left: use brute force or better to generate all paths from c1cx and c2cy Places
#If get_path_time of any pathList is > timeLeft, then delete it
#for all remaining paths, calculate engineScore and onlineScore. 
#weight and add to get pathTotalScore. 
#return path with highest pathTotalScore.


            
def get_path_time(placesPath, finalGate, timeLeft):
    #all in minutes
    #minimum wait times for each category - slightly understated
    #lower wait times result in more suggestions, 
    #allowing the user to make the final call on how much time she has
    #all times in minutes
    minCategoryWaits = [0, 15, 7, 15, 40, 7, 10, 10, 
                   15, 5, 10, 10, 15, 15, 5, 
                   5, 10, 0, 10, 0, 5, 5]
    avgInterGateWalkTime = 0.5
    totalTime = 0
    for i in range(len(placesPath)-1):
        place1 = placesPath[i]
        place2 = placesPath[i+1]
        #get wait time at first place
        waitTime = minCategoryWaits[place1.categoryCode]
        #get walking time
        if place1.terminal == place2.terminal:
            distance = math.fabs(place1.nearestGate-place2.nearestGate)
            walkingTime = distance*avgInterGateWalkTime
            totalTime += waitTime + walkingTime
    lastPlace = placesPath[-1]
    lastWaitTime = minCategoryWaits[lastPlace.categoryCode]
    lastDistance = math.fabs(finalGate - lastPlace.terminal)
    lastTime = lastDistance * avgInterGateWalkTime
    buffer = 0.1 * timeLeft
    totalTime += lastWaitTime + lastDistance + buffer
    return totalTime
            
    
        
    
    