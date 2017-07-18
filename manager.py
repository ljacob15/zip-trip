import things
import extractor
import preferencePreProc
import preferenceEngine
import preferencePostProc
import pathPreProc
import pathConstructor

import datetime


class RecommendationManager():
    def __init__(self, timeWeight = .6, onlineWeight = .4, userPrefWeight = 0, 
                 trainSet = 'userTrainData.xlsx', 
                 testSet = 'userTestData.xlsx', 
                 terminal = 0, flightGate = 17, 
                 currentTime = datetime.datetime(2017,7,18,16,30), 
                 boardingTime = datetime.datetime(2017,7,18,18,30), 
                 location = 34):
        self.timeWeight = timeWeight
        self.onlineWeight = onlineWeight
        self.userPrefWeight = userPrefWeight
        self.trainSet = trainSet
        self.testSet = testSet
        self.terminal = terminal
        self.flightGate = flightGate
        self.timeLeft = boardingTime - currentTime
        self.timeLeft = float(self.timeLeft.seconds)/60.0
        self.location = location
        

    def generate_recommendations(self):

        #bob will be User #1 from the userTestData
        #use the engine to train, test, and get Bob's userTypes
        userTrainDF = extractor.extract_users(filer = self.trainSet)
        userTestDF = extractor.extract_users(filer = self.testSet)
        userTrainMatrix, labels = preferencePreProc.clean_users(userTrainDF)
        userTestMatrix = preferencePreProc.clean_users(userTestDF)
        #return userTrainMatrix, labels, userTestMatrix
        bobProbs = preferenceEngine.predict_user_type(userTrainMatrix, labels, 
                                                     userTestMatrix)
        #c1Categs, c2Categs, timeLeft = pathConstructor.generate_fake_categories()
        #using Bob's userTypes and the weighting file,
        #generate ranked lists of Class 1 and Class 2 categoryCodes
        #this two ranked lists get fed into Phase 2
        c1Categs, c2Categs = preferencePostProc.generate_categs(userTypeWeights = bobProbs)
       
        '''END PHASE 1, START PHASE 2'''
        
        #extract and clean places
        rawPlacesDict = extractor.extract_places(filer = "placeAttributes.xlsx")
        productCodes, foodCodes = pathPreProc.generate_codes()
        cleanPlacesDict = pathPreProc.clean_places(placesDict = rawPlacesDict,
                                                   productCodesDict = productCodes,
                                                   foodCodesDict = foodCodes)
        
        
        #use Bob's ranked Category lists and the timeLeft to generate
        #a list of categories we'd like bob to visit. Then use that list to generate
        #a list of places we'd like bob to visit.
        c1PlacesDict, c2PlacesDict = pathPreProc.get_places(cleanPlacesDict, 
                                                            c1Categs, 
                                                            c2Categs,
                                                            self.terminal, 
                                                            self.timeLeft, 
                                                            self.timeWeight, 
                                                            self.onlineWeight)
        
        return c1PlacesDict, c2PlacesDict
        #from the places, construct paths from current location through Places and to gate.
        #use the search algorithm to find the best path (shortest and best onlineRating)
        '''
        path = pathConstructor.find_path(cleanPlacesDict, c1PlacesDict,
                                         c2PlacesDict, self.flightGate, 
                                         self.location, self.timeLeft)
        

        return path
        '''
        
        
