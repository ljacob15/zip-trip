import math
from itertools import product, permutations
import pdb
import subprocess

class Path():
    def __init__(self, placeTuple, flightGate, location,
                 timeLeft, timeWeight, onlineWeight):
        self.placeList = placeTuple
        self.timeToTake = self.get_path_time(placeTuple, flightGate, location, timeLeft)
        self.avgOnlineScore = self.get_avg_online_score(placeTuple)
        self.totalScore = self.get_total_score(timeWeight, onlineWeight, timeLeft)
        self.timeLeft = timeLeft

    def __str__(self):
        print("Time before boarding: " + str(self.timeLeft))
        print()
        print("Recommended Places:")

        for place in self.placeList:
            print(str(place) + " (nearest gate: " + str(place.nearestGate) + ")" )
        return ''

    def get_path_time(self, placeList, flightGate, location, timeLeft):
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
        firstWalkDistance = math.fabs(placeList[0].nearestGate - location)
        firstWalkTime = firstWalkDistance * avgInterGateWalkTime
        totalTime += firstWalkTime
        #loop through each two adjacent places
        for i in range(len(placeList)-1):
            place1 = placeList[i]
            place2 = placeList[i+1]
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
        lastPlace = placeList[-1]
        floatCode = lastPlace.categoryCode
        intCode = int(floatCode)
        lastWaitTime = intCode
        #get time to walk from last place to flight gate
        lastWalkDistance = math.fabs(flightGate - lastPlace.nearestGate)
        lastWalkTime = lastWalkDistance * avgInterGateWalkTime
        bufferTime = 0.1 * timeLeft
        totalTime += lastWaitTime + lastWalkTime + bufferTime
        return totalTime

    def get_avg_online_score(self, placeList):
        totalScore = 0
        ratedPlaces = 0
        for place in placeList:
            if place.onlineRating != -1:
                totalScore += place.onlineRating
                ratedPlaces += 1
        avgOnlineScore = float(totalScore)/float(ratedPlaces)
        return avgOnlineScore

    def get_total_score(self, timeWeight, onlineWeight, timeLeft):
        '''weights are between 0 and 1, and should add to 1?
        yes because that would ensure that the min score is 0 and max score is 1
        ...highest score wins'''
        #express timeToTake as a percentage of the time remaining
        normalizedTimeToTake = self.timeToTake/timeLeft
        normalizedTimeToTake = 1 - normalizedTimeToTake
        #get the factor to scale the average online rating by
        onlineScalingFactor = timeLeft/5.0
        #scale the avg online score so that the max, 5, equals the timeLeft
        scaledOnlineScore = self.avgOnlineScore * onlineScalingFactor
        #normalize the scaled online score by finding percentage of timeLeft
        normalizedOnlineScore = scaledOnlineScore / timeLeft
        #weight both of the newly scaled scores
        weightedTimeToTake = normalizedTimeToTake * timeWeight
        weightedOnlineScore = normalizedOnlineScore * onlineWeight
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
    combinedDict = {**c1Places, **c2Places}
    categoryPlaceList = []
    for category in combinedDict:
        if len(combinedDict[category]) > 0:
            categoryPlaceList.append(combinedDict[category])
    import pdb; pdb.set_trace()
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

    #eliminate all paths whose time is more than timeLeft
    shortPaths = []
    for path in allPaths:
        if path.timeToTake < timeLeft:
            shortPaths.append(path)
    subprocess.run(['echo', '-n', 'Number of time-bound paths:'])
    subprocess.run(['cat', '\n'],
                   input = str(len(allPaths)), universal_newlines = True)
    subprocess.run('echo')

    #rank the remaining paths by their totalScore
    subprocess.run("echo Sorting paths by totalscore...")
    orderedPaths = sorted(shortPaths,
                          key = lambda x: x.totalScore, reverse = True)

    bestPath = orderedPaths[0]
    return bestPath


    #if not brute force, then greedy! Every next place is the closest place.
    #but this will need to take into account the onlineWeight Somehow.
