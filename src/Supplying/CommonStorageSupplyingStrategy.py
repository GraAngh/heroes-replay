import os
import re
from ..Entities import Toon, Account


class CommonStorageSupplyingStrategy:
    def _commonToonIterator(self, dir):
        for it in os.scandir(dir):
            if not it.is_dir():
                continue
                
            toon = Toon.parse(it.name)
            if toon:
                yield it, toon
            
    def _commonAccountIterator(self, dir):
        # абс. путь
        accounts = os.path.join(dir, 'Accounts')
        if not os.path.exists(accounts): 
            return
            
        for it in os.scandir(accounts):
            if ( it.is_dir() and re.fullmatch(r'^\d+$', it.name ) ):
                yield it, Account.getInstance(it.name)
                
    def supply(self, path, cb):
        for acc_entry, account in self._commonAccountIterator(path):
            for toon_entry, toon in self._commonToonIterator(acc_entry.path):
                account.addToon(toon)
                cb(account, toon)
                        
            