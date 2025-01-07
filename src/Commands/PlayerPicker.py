from .Repr.PlayerRepr import PlayerRepr

# Классу известно в каком виде приходят данные от команды SEARCH

class PlayerPicker:
    def __init__(self, resultSet, length):
        self.__resultSet = resultSet
        self.__len = length
    
    def __formatIndex(self, index):
        i = int( index ) 
        if i < 0 or i >= self.__len:
            raise ValueError('index at outside of range')
        return i
    
   
    def execForInitMode(self, args, rest):
        return None
        
    def execForSearch(self, args, rest):
        try:
            i = self.__formatIndex(rest[0])
        except ValueError as e:
            return None
        
        player = self.__resultSet[i]['player']
        return PlayerRepr(player)
        
    def execForReplay(self, args, rest):
        try:
            i = self.__formatIndex(rest[0])
        except Exception as e:
            return None
        
        player = self.__resultSet[i]
        return PlayerRepr(player)