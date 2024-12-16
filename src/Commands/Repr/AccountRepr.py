class AccountRepr:
   
    def __init__(self, acc, disabledAccounts, disabledToons):
        self.__disabledAccounts = disabledAccounts
        self.__disabledToons = disabledToons
        self.__acc = acc
    
    def getAccount(self):
        return self.__acc
    
    def show(self):
        print('NOt implemented')
        
   