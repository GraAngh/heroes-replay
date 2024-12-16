from ...Entities.Account import Account
from ...Entities.Toon import Toon

class AccountsRepr:
    ACCOUNT_INDENT = '{0:2}'.format(' ')
    TOON_INDENT = '{0:4}'.format(' ')
    
    # result {Dict}
    def __init__(self, pagination, disabledAccounts, disabledToons):
        self.__disabledAccounts = disabledAccounts
        self.__disabledToons = disabledToons
        self.__pagination = pagination
        
        # параметры состояния
        self._isDisabledAccount = False
        self._isDisabledToon = False
        self._currentAccount = None
    
    def getPagination(self):
        return self.__pagination
    
    def lineRepr(self, repr, entity):
        if type(entity) is Account:
            self._currentAccount = entity
            self._isDisabledAccount = (
                entity.getName() in self.__disabledAccounts
            )
            self.accountRepr(repr, entity)
        
        elif type(entity) is Toon:
            self._isDisabledToon = (
                self._isDisabledAccount 
                or entity.toString() in self.__disabledToons
            )   
            self.toonRepr(repr, entity)
    
    def accountRepr(self, index, acc):
        if self._isDisabledAccount:
            print( self.__getDisabledAccStr(index, acc.getName()) )
        else:
            print( self.__getEnabledAccStr(index, acc.getName()) )
        
    def toonRepr(self, index, toon):
        id = toon.getId()
        region = toon.getRegion().name
        realm = toon.getRealm().name
        
        if self._isDisabledToon:
            print( self.__getDisabledToonStr(index, id, region, realm) )
        else:
            print( self.__getEnabledToonStr(index, id, region, realm) )
    
    def __show(self, page):
        if not page:
            return
        for items in page:
            self.lineRepr( *items )
    
    def show(self):
        self.__show(self.__pagination.page())
            
    def hasData(self):
        return True
    
    def __getEnabledToonStr(self, index, id, region, realm):
        return f'{self.TOON_INDENT}{index}. \033[32;1m{id}\033[0m [{region}] [{realm}]'
                
    def __getDisabledToonStr(self, index, id, region, realm):
        return f'\033[30;1m{self.TOON_INDENT}{index}. {id} [{region}] [{realm}]\033[0m'    
        
    def __getEnabledAccStr(self, index, name):
        return f'\n{self.ACCOUNT_INDENT}{index})\033[32m {name}\033[0m\n'        
        
    def __getDisabledAccStr(self, index, name):
        return f'\n\033[30;1m{self.ACCOUNT_INDENT}{index}) {name}\033[0m\n'
    
    #
    # START Pagination >>>>>>>>>>>>>>
    # 
    def at(self, num):
        self.__show( self.__pagination.at(num) )
        
    def forward(self):
        self.__show( self.__pagination.forward() )
        
    def back(self):
        self.__show( self.__pagination.back() )
    
    def first(self, amount):
        self.__pagination.first(amount) 
    # 
    # END Pagination <<<<<<<<<<<<<<<
    #
    