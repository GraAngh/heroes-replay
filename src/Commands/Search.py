from ..Entities import Realm, Region
from ..Config import Config
from .Repr.SearchRepr import SearchRepr
from .Repr.ListPagination import ListPagination
import re

class Search:
    def __init__(self, supplyStrategy):
        self._supplyStrategy = supplyStrategy
        
    def exec(self, args, rest):
        # Предворительное опредление параметров, используемых в команде
        given_name = ''
        given_hero = ''
        given_toonId = 0
        given_regions = [Region.EU.value, Region.AS.value, Region.NA.value]
        given_realms = [Realm.ACTUAL.value]
        ignoreCase = True
        
        flags = 0
        resultSet = []    
        
        # фактическая обработка аргументов
        for o, v in args:
            if o == '-p':
                given_name = v
            elif o == '-i':
                flags = re.I
            elif o == '-t':
                given_toonId = v
            elif o == '-h':
                given_hero = v
            elif o == '-r':
                if int(v) not in regions:
                    regions.append(v)
            elif o == '--ptr': 
                if Realm.PTR not in given_realms:
                    given_realms.append(  )
            elif o == '--ptr-only':
                given_realms = [ Realm.PTR ]
        
        if not given_name and not given_hero and not given_toonId:
            return 
            
        
        # Функция первого порядка для обработки подаваемых повторов
        
        
        # >>> FOR TEST REASON <<<
        # counter = 100
        
        # TODO 
        # - реализовать поиск по герою
        # - реализовать поиск по toonId
        # - реализовать поиск по региону
        # - реализовать поиск по области
        def processReplay(replay, toon, account):
            details = replay.getDetails()
            
            if details == None:
                return 
            
            for player in details.getPlayers():
                if given_name and re.search(given_name, player.getName(), flags):
                    resultSet.append( {
                        'replay': replay,
                        'player': player
                    } )
                    
                    # >>> FOR TEST REASON <<<
                    # nonlocal counter
                    # counter -= 1
                    # if not counter:
                        # return True
        
        config = Config.getInstance(Config.MAIN)
        # Момент организации подачи объектов в обрабатываемую фукнцию
        # (жестко вшитая стратегия подачи)
        for entryDir in config.get('HERO_USERS_DATA_DIRS'):
            if (self._supplyStrategy.supply(
                entryDir
              , processReplay
            )):
                break
        
        return SearchRepr( ListPagination(
            resultSet
          , config.get('PAGE_FIRST_ITEMS_REPR')
        ) )