import math

class Place():
    def __init__(self, attributeDict):
        # self.id =
        # self.name = name
        # self.terminal = terminal
        # self.className = className
        # self.category = category
        self.terminal = None
        for item in attributeDict:
            setattr(self, item, attributeDict[item])

    def __str__(self):
        try:
            return (self.placeName)
        except:
            raise NameError("Place has no name.")

    def get_id(self):
        try:
            return self.placeID
        except:
            raise ValueError("Place has no id")

    def get_terminal(self):
        try:
            return self.terminal
        except:
            raise ValueError("Place has no terminal")

    def get_class(self):
        try:
            return self.classCode
        except:
            raise ValueError("Place has no class")

    def get_category(self):
        try:
            return self.categoryCode
        except:
            raise ValueError("Place has no category")

class User():
    def __init__(self, attributeDict = None):
        """User Demographics: gender, age, type, avgTrips, kids, cabinPreference,
        avgDuration, numDomestic, percentDomestic, PAXTrips, percentAccompanied"""
        for item in attributeDict:
            setattr(self, item, attributeDict[item])

    def __str__(self):
        try:
            return (self.ID)
        except:
            raise NameError("User has no ID.")


def create_fake_user():
    attributeDict = {}
    keyList = ['userID', 'userName', 'gender', 'travelType',
               'preferredCategoryCodes',
               'preferredFoodCodes', 'preferredProductCodes',
               'topAmenities', 'airlineStatus', 'location']
    valueList = ["17", "Jim", "male", "leisure",
                 [1,2,3,4,5], [4,6,8,13,17], [1,5,6],
                 ['water', 'reading', 'tech'], 'platinum', None]
    for i in range(len(keyList)):
        key = keyList[i]
        value = valueList[i]
        attributeDict[key] = value

    Bob = User(attributeDict)
    return Bob


class Trip(User):
    def __init__(self, gateLocation, boardingTime, checkinTime):
        super.__init__()
        self.gateLocation = gateLocation
        self.boardingtime = boardingTime
        self.checkinTime = checkinTime
        #list of Places the user visited on that trip
        self.placesVisited = []


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
        '''
        minimum wait times for each category - slightly understated
        lower wait times result in more suggestions,
        allowing the user to make the final call on how much time she has
        all times in minutes
        '''
        minCategoryWaits = [0, 15, 7, 15, 40, 7, 10, 10,
                       15, 5, 10, 10, 15, 15, 5,
                       5, 10, 0, 10, 0, 5, 5]
        avgInterGateWalkTime = 0.3
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
        # bufferTime = 0.1 * self.timeLeft
        totalTime += lastWaitTime + lastWalkTime  # + bufferTime

        return totalTime

    def calc_avg_online_score(self):
        totalScore = 0
        ratedPlaces = 0
        for place in self.placeList:
            if place.onlineRating != -1:
                totalScore += place.onlineRating
                ratedPlaces += 1
        avgOnlineScore = float(totalScore)/float(ratedPlaces)

        self.avgOnlineScore = avgOnlineScore
        return None

    def calc_total_score(self):
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

        self.totalScore = totalScore

        return None

    def get_place_names(self):
        placeNames = []
        for place in self.placeList:
            placeNames.append(place.placeName)

        return placeNames
