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
        self.gateLocation = gateLocation
        self.boardingtime = boardingTime
        self.checkinTime = checkinTime
        #list of Places the user visited on that trip
        self.placesVisited = []
