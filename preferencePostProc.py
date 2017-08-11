import things

import pandas as pd
import numpy as np
import pdb


def generate_categs(filer = 'userTypeCategoryWeights.xlsx', userTypeWeights = None):
    assert type(userTypeWeights) == list, "userTypeWeights is not a list"

    #lists of Class 1 and Class 2 categories
    #currently includes only categories we have DFW place data for
    #although there are a few more categories in 'userTypeCategoryWeights.xlsx'
    c1Categs = [2, 3, 4, 6, 7, 21]
    c2Categs = [5, 8, 9, 10, 11, 12, 13,] #18, 19,]
    weightTable = pd.read_excel(filer, header = 0, index_col = 0)
    weightTable2 = weightTable.drop(labels = "description", axis = 1)

    #multiple userType values (from machine) by userType weights for each category
    for i in range(len(userTypeWeights)):
        weight = userTypeWeights[i]
        userType = i+1
        for row in weightTable2.index:
            weightTable2.loc[row,userType] *= weight
    categoryScoreList = []

    #for each category
    for row in weightTable2.index:
        categoryScore = 0
        #for each userType
        for column in weightTable2.columns:
            categoryScore += weightTable2.loc[row,column]
        categoryScoreList.append(categoryScore)

    #order the categories by their preference rating    
    c1OrderedCategs = sorted(c1Categs,
                             key = lambda x: categoryScoreList[x],
                             reverse = True)
    c2OrderedCategs = sorted(c2Categs,
                             key = lambda x: categoryScoreList[x],
                             reverse = True)

    return c1OrderedCategs, c2OrderedCategs
