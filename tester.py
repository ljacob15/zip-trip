import manager


def main():
    #Bob = things.create_fake_user()
    rm = manager.RecommendationManager()
    final = rm.generate_recommendations()
    return final


if __name__=='__main__':
    from datetime import datetime
    startTime = datetime.now()
    result = main()
    print()
    print("Recommended Places:")
    print()
    for item in result:
        print(item)
    endTime = datetime.now()
    print("Time Taken = " + str(endTime - startTime))
