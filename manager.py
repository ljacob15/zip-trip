import things
import extractor
import preferencePreProc
import preferenceEngine
import preferencePostProc
import pathPreProc
import pathConstructor

from datetime import datetime
import subprocess
import io
import pdb


class RecommendationManager():
    def __init__(self, timeWeight = .65, onlineWeight = .35, userPrefWeight = 0,
                 trainSet = 'userTrainData.xlsx',
                 testSet = 'userTestData.xlsx',
                 terminal = 0, flightGate = 17,
                 currentTime = datetime(2017,7,19,9,00),
                 boardingTime = datetime(2017,7,19,11,00),
                 location = 34,
                 userFoodCodes = None):
        self.timeWeight = timeWeight
        self.onlineWeight = onlineWeight
        self.userPrefWeight = userPrefWeight
        self.trainSet = trainSet
        self.testSet = testSet
        self.terminal = terminal
        self.flightGate = flightGate
        self.currentTime = currentTime
        self.boardingTime = boardingTime
        self.timeLeft = boardingTime - currentTime
        self.timeLeft = float(self.timeLeft.seconds)/60.0
        self.location = location
        self.userFoodCodes = userFoodCodes

    def generate_recommendations(self):

        #Robert will be User #1 from the userTestData
        #use the engine to train, test, and get Robert's userTypes
        userTrainDF = extractor.extract_users(filer = self.trainSet)
        # print("Training set constructed")
        proc = subprocess.run("echo Training set constructed")

        userTestDF = extractor.extract_users(filer = self.testSet)
        # print("Testing set constructed")
        subprocess.run("echo Testing set constructed")

        userTrainMatrix, labels = preferencePreProc.clean_users(userTrainDF)
        userTestMatrix = preferencePreProc.clean_users(userTestDF)
        # print("Training and testing sets cleaned")
        subprocess.run("echo Training and testing sets cleaned")

        #return userTrainMatrix, labels, userTestMatrix
        RobertProbs = preferenceEngine.predict_user_type(userTrainMatrix, labels,
                                                     userTestMatrix)
        RobertOut = str(RobertProbs)
        # print("Robert's preferences predicted:")
        subprocess.run("echo Robert's preferences predicted:")
        subprocess.run('cat', input = RobertOut, universal_newlines = True)
        subprocess.run('echo')

        # print(RobertProbs)

        #using Robert's userTypes and the weighting file,
        #generate ranked lists of Class 1 and Class 2 categoryCodes
        c1Categs, c2Categs = preferencePostProc.generate_categs(userTypeWeights = RobertProbs)
        c1Out = str(c1Categs)
        c2Out = str(c2Categs)
        # print("Robert's preferred ordered categories generated:")
        subprocess.run("echo Robert's preferred ordered categories generated:")
        subprocess.run('cat', input = c1Out, universal_newlines = True)
        subprocess.run('cat', input = c2Out, universal_newlines = True)
        subprocess.run('echo')


        '''END PHASE 1, START PHASE 2'''

        #extract and clean places
        rawPlacesDict = extractor.extract_places(filer = "placeAttributes.xlsx")
        productCodes, foodCodes = pathPreProc.generate_codes()
        cleanPlacesDict = pathPreProc.clean_places(placesDict = rawPlacesDict,
                                                   productCodesDict = productCodes,
                                                   foodCodesDict = foodCodes)
        # print("Airport Places constructed and cleaned")
        subprocess.run("echo Airport Places constructed and cleaned")

        #use Robert's ranked Category lists and the timeLeft to generate
        #a narrowed down list of categories we'd like Robert to visit.
        #Then use that list to generate a list of specific places Robert might like to visit.
        c1PlacesDict, c2PlacesDict, preferredPlaces = pathPreProc.get_places(cleanPlacesDict,
                                                                            c1Categs,
                                                                            c2Categs,
                                                                            self.terminal,
                                                                            self.location,
                                                                            self.timeLeft,
                                                                            self.currentTime,
                                                                            self.userFoodCodes)
        if preferredPlaces:
            placeNames = []
            for place in preferredPlaces:
                placeNames.append(place.placeName)
            subprocess.run("echo Robert's new preferences:")
            subprocess.run('cat', input = str(placeNames), universal_newlines = True)
            subprocess.run('echo')
            return "Done!"


        #from the places, construct paths from current location through Places and to gate.
        #use the search algorithm to find the best path (shortest and best onlineRating)
        bestPath = pathConstructor.find_path(cleanPlacesDict, c1PlacesDict,
                                         c2PlacesDict, self.flightGate,
                                         self.location, self.timeLeft,
                                         self.timeWeight, self.onlineWeight)
        return bestPath
