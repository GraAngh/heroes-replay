from .Repr.AccountsRepr import AccountsRepr
from .Repr.ObjectPointer import ObjectPointer
from .Repr.NestedPagination import NestedPagination
from ..Config import Config

DISABLED_ACCOUNTS = 'DISABLED_ACCOUNTS'
DISABLED_TOONS = 'DISABLED_TOONS'
PAGE_FIRST = 'ACCOUNTS_FIRST_ITEMS_REPR'
USERS_DATA_DIRS = 'HERO_USERS_DATA_DIRS'

class Accounts:
    def __init__(self, supplyStrategy):
        self.__supplyStrategy = supplyStrategy
        self.__accounts = []
    
    def exec(self, args, rest):
        userStates = Config.getInstance( Config.USER_STATES )
        
        def collect_accounts(acc, toon):
            if acc not in self.__accounts: 
                self.__accounts.append(acc)
        
        config = Config.getInstance(Config.MAIN)
        for entryDir in config.get(USERS_DATA_DIRS):
            self.__supplyStrategy.supply(entryDir, collect_accounts)
        
        pagination = NestedPagination(
            ObjectPointer(self.__accounts, [lambda a: a.getToons()], 2)
          , config.get(PAGE_FIRST)
        )
        
        return AccountsRepr(
            pagination
          , userStates.get(DISABLED_ACCOUNTS)
          , userStates.get(DISABLED_TOONS)
        )