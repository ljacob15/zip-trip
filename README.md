# zip-trip
ZipTripAPI From Sabre 2017 Intern Case Competition


The goal of this API is to recommend to a user places in DFW Airport that said user is likely to enjoy. 

The engine combines a KNN machine learning alogrithm (to maximize preferences) with a (currently brute force) 
shortest path algorithm (to maximize time efficiency). 

The engine should return a list of places in the airport that User is likely to enjoy. 
The list should follow a rough path from User's current location to User's departure gate.
