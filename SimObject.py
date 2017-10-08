#from peter import *
import datetime

Infinite = float("inf") # hug value

class SimObject(object):
    # Object ID which tracks the entire instantiated Objects
    __GLOBAL_OBJECT_ID = 0

    def __init__(self):
        self.__created_time = datetime.datetime.now()
        self.__object_id = SimObject.__GLOBAL_OBJECT_ID
        SimObject.__GLOBAL_OBJECT_ID = SimObject.__GLOBAL_OBJECT_ID + 1

    def __str__(self):
        return "ID:%10d %s" % self.__object_id, self.__created_time