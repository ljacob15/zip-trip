import manager
from datetime import datetime
import subprocess

def main():
    #Robert = things.create_fake_user()
    messages = ["echo Standard Engine: When Robert clears security",
                "echo Updated Engine: When Robert's flight is delayed",
                "echo Updated Engine: When Robert changes his preferences"]
    engines = [manager.RecommendationManager(),
               manager.RecommendationManager(currentTime = datetime(2017,7,19,9,20),
                                             boardingTime = datetime(2017,7,19,12,00),
                                             location = 30),
               manager.RecommendationManager(currentTime = datetime(2017,7,19,9,22),
                                             boardingTime = datetime(2017,7,19,12,00),
                                             location = 30,
                                             userFoodCodes = [0,6])
               ]
    for i in range(3):
        run(messages[i], engines[i])

def run(initialMessage, engine):
    subprocess.run(initialMessage)
    print()
    startTime = datetime.now()
    rm = engine
    final = rm.generate_recommendations()
    endTime = datetime.now()
    input("Process complete. Press Enter for engine output.")
    print("-------------------------")
    print(final)
    print("Total Time Taken = " + str(endTime - startTime))
    print()
    input("Press Enter to continue...")

result = main()
