from things import Path

import math
from itertools import product, permutations
import pdb
import subprocess

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

    #eliminate all paths whose time is more than timeLeft
    shortPaths = []
    for path in allPaths:
        if path.timeToTake < timeLeft:
            shortPaths.append(path)

    assert len(shortPaths) > 0, "All paths take too long..."

    for path in shortPaths:
        path.calc_avg_online_score()
        path.calc_total_score()

    # import pdb; pdb.set_trace()

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
