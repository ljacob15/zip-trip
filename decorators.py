#decorators
import time

def timer(function):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = function(*args, **kwargs)
        end = time.time()
        timeTaken = end-start
        return res, timeTaken
    return wrapper
