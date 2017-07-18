import things

import pandas as pd
import numpy as np


def generate_categs(filer = 'userTypeCategoryWeights.xlsx', userTypeWeights = None):
    assert type(userTypeWeights) == list, "userTypeWeights is not a list"
    #lists of Class 1 and Class 2 categories
    #current includes only categories Ray has data for
    #although there are a few more categories on the weightTable
    c1Categs = [2, 3, 4, 6, 7, 21]
    c2Categs = [5, 8, 9, 10, 11, 12, 13,] #18, 19,]
    weightTable = pd.read_excel(filer, header = 0, index_col = 0)
    weightTable = weightTable.drop(labels = "description", axis = 1)
    for weight in userTypeWeights:
        userType = userTypeWeights.index(weight)+1
        for row in weightTable.index:
            weightTable.loc[row,userType] *= weight
    categoryScoreList = []
    for row in weightTable.index:
        categoryScore = 0
        for column in weightTable.columns:
            categoryScore += weightTable.loc[row,column]
        categoryScoreList.append(categoryScore)
    c1OrderedCategs = sorted(c1Categs, 
                             key = lambda x: categoryScoreList[x], 
                             reverse = True)
    c2OrderedCategs = sorted(c2Categs, 
                             key = lambda x: categoryScoreList[x], 
                             reverse = True)
    return c1OrderedCategs, c2OrderedCategs
    
            