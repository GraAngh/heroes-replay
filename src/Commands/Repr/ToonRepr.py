class ToonRepr:
    def __init__(self, toon, disabledAccounts, disabledToons):
        self.__disabledAccounts = disabledAccounts
        self.__disabledToons = disabledToons
        self.__toon = toon
        
    def getToon(self):
        return self.__toon
    
    def show(self):
        print('NOt implemented')
            