import os
import re
from ..Entities import Toon, Account
from .CommonStorageSupplyingStrategy import CommonStorageSupplyingStrategy as CSSS


class CommonReplaySupplyingStrategy(CSSS):
    def __init__(self, replayCreater, disabledAccounts, disabledToons):
        self.__creater = replayCreater
        self.__disabledAccounts = disabledAccounts
        self.__disabledToons = disabledToons

    def _feedReplay(self, dir):
        for it in os.scandir(dir):
            if it.is_dir():
                for replay in self._feedReplay( it.path ):
                    yield replay
            else:
                yield self.__creater.create( it.path )

    # TODO сделать функцию рекурсивной, для дполонительно вложенных папок 
    def _commonReplayIteratorWrapper(self, dir):
        replays = os.path.join(dir, 'Replays', 'Multiplayer')
        if not os.path.exists(replays): 
            return
        
        for replay in self._feedReplay(replays):
            yield replay
        
    # обробатывая все повторы, мне не известны их имена и не нужно это знать,
    # но когда хочу посмотреть конкретный повтор, то нужен механизм разрешения имени:
    # - это нужно указать имя повтора
    # - аккаунт
    # - toon
    """
    @TODO:
    
    - итерация в соотвествии с параметром config:
    в нем задается допустиыме регионы, область серверов, 
    конкретные аккаунты, конкретные toons
    
    
    @param {str} path - путь к директории как точке входа
    
    """
    def supply(self, path, cb):
        # entry point указывает на папку accounts heroes of the storm
        # Accounts
        # +--+ \d+ папка, именнованная id аккаунта <<< итерация по аккаунтам
        # |    +-- \d as region-Heore-\d as realm-\d+ as toonId <<< итерация по экземплярам в регионах
        # |        +-- Replays 
        # |               +-- Multyplayer
        # |                   +-- replays.files <<< Итерация по реплеям
        # |                       ...
        # |        
        # +-- ...
        #
        for accountDir, account in self._commonAccountIterator( path ):
            accName = account.getName()
            # проверка на исключение обработки аккаунта
            if accName in self.__disabledAccounts:
                continue
            
            for toonDir, toon in self._commonToonIterator( accountDir.path ):
                account.addToon(toon)
                
                # проверка на исключение обработки туна
                if (
                    accName in self.__disabledToons and
                    toon.getId() in self.__disabledToons[accName]
                ):
                    continue

                for replay in self._commonReplayIteratorWrapper( toonDir.path ):
                    if not replay:
                        continue
                    # для тестовых случаев возможность прервать
                    if cb(replay, toon, account):
                        print('СООБЩЕНИЕ: Прерывание подачи')
                        return True
        