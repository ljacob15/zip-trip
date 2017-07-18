from sklearn.neighbors import KNeighborsClassifier


def predict_user_type(trainMatrix, labels, testMatrix,):
#    import pdb; pdb.set_trace()
    clf = KNeighborsClassifier(n_neighbors = 10, weights = 'distance')
    clf.fit(trainMatrix, labels)
    bob = testMatrix[0]
    bob = bob.reshape(1,-1)
    predictions = clf.predict_proba(bob)
    predictions = predictions.reshape(-1)
    predictions = predictions.tolist()
    return predictions