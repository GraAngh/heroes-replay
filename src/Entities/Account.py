"""
   `Account` может содержать множество `Toon`
   `Toon` содержит множество `Player`
"""

class Account:
    _accounts = {}
    
    @staticmethod
    def getInstance(name):
        if name not in Account._accounts:
            Account._accounts[name] = Account(name)
        
        return Account._accounts[name]
        
    def __init__(self, name, toons = []):
        self._toons = []
        self._name = name
    
    def addToon(self, toon, reciprocal = True):
        for t in self._toons:
            if t.toString() == toon.toString():
                return
                
        self._toons.append(toon)
        if reciprocal:
            toon.setAccount(self, False)
        
    def getToons(self):
        return self._toons
    
    def getName(self):
        return self._name
    