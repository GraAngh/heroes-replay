from enum import Enum

class Region(Enum):
    NA = 1
    EU = 2
    AS = 3
    
    @staticmethod
    def getName(num):
        return Region( int(num) ).name