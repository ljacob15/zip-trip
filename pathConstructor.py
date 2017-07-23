import math
from itertools import product, permutations
import pdb
import subprocess

class Path():
    def __init__(self, placeTuple, flightGate, location,
                 timeLeft, timeWeight, onlineWeight):
        self.placeList = list(placeTuple)
        self.flightGate = flightGate
        self.location = location
        self.timeLeft = timeLeft
        self.timeWeight = timeWeight
        self.onlineWeight = onlineWeight

        self.sort_path()
        self.timeToTake = self.get_path_time()
        self.avgOnlineScore = self.get_avg_online_score()
        self.totalScore = self.get_total_score()

    def __str__(self):
        print("Time before boarding: " + str(self.timeLeft))
        print()
        print("Recommended Places:")

        for place in self.placeList:
            print(str(place) + " (nearest gate: " + str(place.nearestGate) + ")" )
        return ''

    def sort_path(self):
        '''placeList: list of places constituting a path
        operation: orders the path based on distance from user
        returns: orderedPlaceList '''
        self.placeList = sorted(self.placeList,
                                key = lambda x: math.fabs(x.nearestGate - self.location))

    def get_path_time(self):
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
        #get time to walk to first place
        firstWalkDistance = math.fabs(self.placeList[0].nearestGate - self.location)
        firstWalkTime = firstWalkDistance * avgInterGateWalkTime
        totalTime += firstWalkTime
        #loop through each two adjacent places
        for i in range(len(self.placeList)-1):
            place1 = self.placeList[i]
            place2 = self.placeList[i+1]
            assert place1.terminal == place2.terminal, "places in different terminals"
            #get wait time at first place
            floatCode = place1.categoryCode
            intCode = int(floatCode)
            waitTime = minCategoryWaits[intCode]
            #get walking time to the next place
            distance = math.fabs(place2.nearestGate-place1.nearestGate)
            walkingTime = distance*avgInterGateWalkTime
            totalTime += waitTime + walkingTime
        #get wait time for last Place
        lastPlace = self.placeList[-1]
        floatCode = lastPlace.categoryCode
        intCode = int(floatCode)
        lastWaitTime = minCategoryWaits[intCode]
        #get time to walk from last place to flight gate
        lastWalkDistance = math.fabs(self.flightGate - lastPlace.nearestGate)
        lastWalkTime = lastWalkDistance * avgInterGateWalkTime
        bufferTime = 0.1 * self.timeLeft
        totalTime += lastWaitTime + lastWalkTime + bufferTime
        return totalTime

    def get_avg_online_score(self):
        totalScore = 0
        ratedPlaces = 0
        for place in self.placeList:
            if place.onlineRating != -1:
                totalScore += place.onlineRating
                ratedPlaces += 1
        avgOnlineScore = float(totalScore)/float(ratedPlaces)
        return avgOnlineScore

    def get_total_score(self):
        '''weights are between 0 and 1, and should add to 1?
        yes because that would ensure that the min score is 0 and max score is 1
        ...highest score wins'''
        #express timeToTake as a percentage of the time remaining
        normalizedTimeToTake = self.timeToTake/self.timeLeft
        normalizedTimeToTake = 1 - normalizedTimeToTake
        #get the factor to scale the average online rating by
        onlineScalingFactor = self.timeLeft/5.0
        #scale the avg online score so that the max, 5, equals the timeLeft
        scaledOnlineScore = self.avgOnlineScore * onlineScalingFactor
        #normalize the scaled online score by finding percentage of timeLeft
        normalizedOnlineScore = scaledOnlineScore / self.timeLeft
        #weight both of the newly scaled scores
        weightedTimeToTake = normalizedTimeToTake * self.timeWeight
        weightedOnlineScore = normalizedOnlineScore * self.onlineWeight
        #calculate final total Score
        totalScore = weightedTimeToTake + weightedOnlineScore
        return totalScore

    def get_place_names(self):
        placeNames = []
        for place in self.placeList:
            placeNames.append(place.placeName)
        return placeNames

def find_path(cleanPlacesDict, c1Places, c2Places,
              flightGate, location, timeLeft, timeWeight, onlineWeight):
    '''cleanPlacesDict = dictionary of places with clean, numerical codes
    c1Places = Ordered Dictionary mapping C1 categories to Places in those
    categories. Same for c2Places.
    flightGate = int representing flight gate
    location = int representing nearest gate
    timeLeft = time left in minutes
    timeWeight = weighting factor to use for time metric for each path
    onlineWeight = weighting factor to use for online rating for each path
    operation: uses brute force to construct all possible paths from user
    through one place in each category and to the Gate.
    Finds best path regarding distance and online rating.'''
    #combine the two dictionaries and turn into a (simpler) list of lists
    combinedDict = {**c1Places, **c2Places}
    categoryPlaceList = []
    for category in combinedDict:
        if len(combinedDict[category]) > 0:
            categoryPlaceList.append(combinedDict[category])
    #get all combinations
    combos = []
    for path in product(*categoryPlaceList):
        combos.append(path)
    allPaths = []
    #without permutations
    for path in combos:
        pathObject = Path(path, flightGate, location, timeLeft,
                          timeWeight, onlineWeight)
        allPaths.append(pathObject)

    #with permutations
    # for path in combos:
    #     for ordering in permutations(path):
    #         pathObject = Path(ordering, flightGate, location, timeLeft,
    #                           timeWeight, onlineWeight)
    #         allPaths.append(pathObject)

    # print("Number of possible paths:" + str(len(allPaths)))
    subprocess.run(['echo', '-n', 'Number of possible paths:'])
    subprocess.run(['cat', '\n'],
                   input = str(len(allPaths)), universal_newlines = True)
    subprocess.run('echo')

    # testing function
    # def different(oldPathList, newPathList):
    #     for i in range(len(oldPathList)):
    #         oldPath = oldPathList[i]
    #         newPath = newPathList[i]
    #         for j in range(len(oldPath.placeList)):
    #             if oldPath.placeList[j] != newPath.placeList[j]:
    #                 return True
    #     return False

    #eliminate all paths whose time is more than timeLeft
    shortPaths = []
    for path in allPaths:
        if path.timeToTake < timeLeft:
            shortPaths.append(path)

    subprocess.run(['echo', '-n', 'Number of time-bound paths:'])
    subprocess.run(['cat', '\n'],
                   input = str(len(shortPaths)), universal_newlines = True)
    subprocess.run('echo')

    #rank the remaining paths by their totalScore
    subprocess.run("echo Sorting paths by totalscore...")
    orderedPaths = sorted(shortPaths,
                          key = lambda x: x.totalScore, reverse = True)

    bestPath = orderedPaths[0]
    return bestPath
