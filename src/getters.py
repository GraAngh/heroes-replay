import os
import json
from subprocess import Popen, PIPE
import re

import src.finders
import src.conditions
import src.Entites


def feedReplay(dir):
    for it in os.scandir(dir):
        if it.is_dir():
            for replay in feedReplay(it.path):
                yield replay
        elif conditions.isInitialReplay(it):
            yield it

# TODO сделать функцию рекурсивной, для дполонительно вложенных папок 
def commonReplayIterator(dir):
    replaysDir = os.path.join(dir, 'Replays', 'Multiplayer')
    if not os.path.exists(replaysDir): 
        return
    
    for replay in feedReplay(replaysDir):
        yield replay.path
    
def commonToonIterator(dir):
    for it in os.scandir(dir):
        if not it.is_dir():
            continue
            
        match = matchToon(it.name)
        if match:
            yield it, match.group('id'), match.group('region'), match.group('realm')
        
def commonAccountIterator(dir):
    accounts = os.path.join(dir, 'Accounts')
    if not os.path.exists(accounts): 
        return
        
    for it in os.scandir(accounts):
        if ( it.is_dir() and re.fullmatch(r'^\d+$', it.name ) ):
            yield it   

def commonReplayStorageIterator(entryDir, cb):
    for account in commonAccountIterator(entryDir):
        for toon, toonId, region, realm in commonToonIterator(account):
            cb(account.name, toonId, region, realm)

# обробатывая все повторы, мне не известны их имена и не нужно это знать,
# но когда хочу посмотреть конкретный повтор, то нужен механизм разрешения имени:
# - это нужно указать имя повтора
# - аккаунт
# - toon
"""
@ TODO
- итерация в соотвествии с параметром config:
    в нем задается допустиыме регионы, область серверов, конкретные аккаунты, конкретные toons
"""
def commonReplayDeliveryStrategy(entryDir, cb, config = None):
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
    for account in commonAccountIterator( entryDir ):
        
        # @ TODO Добавить проверку на исключаемый аккаунт
        
        for toon, toonId, region, realm in commonToonIterator( account.path ):

            # @TODO Добавить проверку на исключаемый toon

            for replay in commonReplayIterator( toon.path ):
                if cb( 
                    replay
                  , account.name
                  , toonId
                  , region
                  , realm
                ):
                    print('завершение подачи повторов')
                    return

def directDirsReplayDeliveryStrategy(dirs, cb):
    if type(dirs) is not list:
        raise TypeError('ожидается список директорий')

    for d in dirs:
        for f in os.scandir(d):
            if conditions.isInitialReplay(f):
                if cb( f ):
                    print('завершение подачи повторов')
                    return

def cachedDataDeliveryStrategy(dir, cb):
    for d in dir:
        for f in os.scandir(d):
            if cb( f ):
                print('завершение подачи повторов')
                return
                

def replayKey(file):
    dir, base =  os.path.split( file )
    return os.path.splitext( base )[0]

def heroprotocolCall(replayFile, arg):
    p1 = Popen(["python", "-m", "heroprotocol", "--json", "--" + arg, replayFile], stdout = PIPE)
    data = p1.stdout.read()
    return data.decode('utf-8')

def heroDataMapper(data, arg):
    match arg:
        case HeroArg.DETAILS:
            return Entites.Details( data )
        case HeroArg.INIT_DATA:
            return Entites.InitData( data )
        case HeroArg.HEADER:
            return Entites.Header( data )
        case HeroArg.ATTR_EVENTS:
            return Entites.AttributeEvents( data )
        case HeroArg.TRACKER_EVENTS:
            return Entites.TrackerEvents( data )
        case HeroArg.GAME_EVENTS:
            return Entites.GameEvents( data )
        case HeroArg.MESSAGE_EVENTS:
            return Entites.MessageEvents( data )
        case _:
            raise ValueError(f"Неизвестная команда {arg}")
            

