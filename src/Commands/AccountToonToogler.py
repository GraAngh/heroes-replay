import re, sys
from ..Config import Config
from ..Entities import Account, Toon

class AccountToonToogler:
    def __init__(self):
        pass
    
    def toogleByPointer(self, args, rest, objectPointer):
        pointer = []
        for string in rest:
            try:
                i = int(string)
            except ValueError as err:
                print(
                    f'[ERROR] {err}\n' 
                  + f'[ERROR] Use digits separated with spaces to index like \'2 1 3\''
                  , file=sys.stderr)
                return                
            pointer.append( i )
        obj = objectPointer.at(pointer)
        if not obj:
            return
        t = type(obj)
        if t is Account:
            self.toogleAccount(obj)
        elif t is Toon:
            self.toogleToon(obj)
        else:
            raise TypeError('Must be *Account* or *Toon*. Has passed ' + t)
    
    def toogleAccount(self, account):
        self.__exec( account.getName(), 'DISABLED_ACCOUNTS' )
        
    def toogleToon(self, toon):
        self.__exec( toon.toString(), 'DISABLED_TOONS' )
    
    def __exec(self, objRepr, containerName):
        userStates = Config.getInstance( Config.USER_STATES )
        container = userStates.get(containerName)
        if objRepr in container:
            del container[objRepr]
        else:
            container[objRepr] = True 
            