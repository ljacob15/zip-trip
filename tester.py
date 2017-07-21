import manager
from datetime import datetime


def main():
    #Bob = things.create_fake_user()

    print("Standard Engine: When Bob clears security")
    startTime = datetime.now()
    rm = manager.RecommendationManager()
    finalOne = rm.generate_recommendations()
    endTime = datetime.now()
    printer(finalOne)
    print("Time Taken = " + str(endTime - startTime))
    print()

    input("Press Enter to continue...")

    print("Updated Engine: When Bob's flight is delayed")
    print()
    print("Working...")
    print()
    startTime = datetime.now()
    rm = manager.RecommendationManager(boardingTime = datetime(2017,7,19,1,00))
    finalTwo = rm.generate_recommendations()
    endTime = datetime.now()
    printer(finalTwo)
    print("Time Taken = " + str(endTime - startTime))
    print()

    input("Press Enter to continue...")

    print("Updated Engine: When Bob changes his preferences")
    startTime = datetime.now()
    rm = manager.RecommendationManager(boardingTime = datetime(2017,7,19,1,00),
                                       userFoodCodes = [15])
    finalThree = rm.generate_recommendations()
    endTime = datetime.now()
    printer(finalThree)
    print("Time Taken = " + str(endTime - startTime))


    return finalOne, finalTwo, finalThree

def printer(result):
    print()
    print("Recommended Places:")
    print()
    for item in result:
        print(item)


result = main()
