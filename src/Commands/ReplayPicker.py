from .Repr.ReplayRepr import ReplayRepr

# Классу известно в каком виде приходят данные от команды SEARCH

class ReplayPicker:
    def __init__(self, replays, resultLength):
        self.__replays = replays
        self.__resultLength = resultLength
        
    def exec(self, args, rest):
        
        try:
            i = int( rest[0] ) 
        except ValueError as e:
            return None
            
        if i < 0 or i >= self.__resultLength:
            return None
        replay = self.__replays[i]['replay']
        return ReplayRepr(replay)
    