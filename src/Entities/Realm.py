from enum import Enum

class Realm(Enum):
    ACTUAL = 1
    PTR = 2
    
    @staticmethod
    def getName(num):
        return Realm( int(num) ).name