import things
import placeExtractor
import preferencePreProc
import preferenceEngine
import pathPreProc
import pathConstructor

import datetime


class RecommendationManager():
    def __init__(self, user = None, engineWeight = .5, popularityWeight = .5,
                 timeWeight = .5, qualityWeight = .5):
        self.user = user
        #weights for preference generator
        self.engineWeight = engineWeight
        self.popularityWeight = popularityWeight
        #weights for path generator
        self.timeWeight = timeWeight
        self.qualityWeight = qualityWeight

    def generate_recommendations(self):
        rawPlacesDict = placeExtractor.extract_places()
        productCodes, foodCodes = preferencePreProc.generate_codes()
        cleanPlacesDict = preferencePreProc.clean_places(placesDict = rawPlacesDict,
                                                         productCodesDict = productCodes, 
                                                         foodCodesDict = foodCodes)
        c1Categs, c2Categs, timeLeft = pathConstructor.generate_fake_categories()
        c1cxPlaces, c2cyPlaces = pathConstructor.find_path(cleanPlacesDict,
                                                           c1Categs, 
                                                           c2Categs,
                                                           terminal = 0, 
                                                           gate = 20, 
                                                           timeLeft = timeLeft)
        return c1cxPlaces, c2cyPlaces
                                                           

        #matrix = preferencePreProc.pre_process(placesDict)
        #feed the matrix into the engine
        #preferenceEngine.trainModel()
