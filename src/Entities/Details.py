from .Color import Color
from .Toon import Toon
from .Player import Player
from .Team import Team
from datetime import datetime as dt
from src.utils import winTicksToUnixTime

# как фабричный класс    
class Details:
    __fields__ = [
        "m_cacheHandles"            # { list:dict }
      , "m_defaultDifficulty"       # { int:7 }
      , "m_difficulty"              # { str:"" }
      , "m_gameSpeed"               # { int:4 }
      , "m_isBlizzardMap"           # { bool:true }
      , "m_mapFileName"             # { str:"" }
      , "m_miniSave"                # { bool:false }
      , "m_modPaths"                # { :null }
      , "m_playerList"              # { list }
      , "m_restartAsTransitionMap"  # { bool:false }
      , "m_thumbnail"               # { dict }
      , "m_timeLocalOffset"         # { ts }
      , "m_timeUTC"                 # { ts }
      , "m_title"                   # { str }
    ]
    
    MAPS = {
        'RU': {
            # regular
            'SPIDERS' : 'Гробница Королевы Пауков',
            'FOUNDRY' : 'Завод Вольской',
            'SHRINES' : 'Оскверненные святилища',
            'BATTLE'  : 'Вечная битва',
            'HANAMURA': 'Храм Ханамуры',
            'BRAXIS'  : 'Бойня на Браксисе',
            'DRAGON'  : 'Драконий край',
            'ALTERAC' : 'Альтеракский перевал',
            'BAY'     : 'Бухта Черносерда',
            'HOLLOW'  : 'Проклятая лощина',
            'TOWERS'  : 'Башни Рока',
            'WARHEAD' : 'Ядерный полигон',
            'GARDEN'  : 'Сад ужасов',
            'MINES'   : 'Призрачные Копи',
            'SKY'     : 'Небесный храм',
            # aram
            'INDUSTRIAL': 'Промзона',
            'OUTPOST'  : 'Аванпост на Браксисе',
            'CAVERN'   : 'Затерянный грот',
            'SILVER'   : 'Серебряный город',
            # sandbox
            'S_HOLLOW': 'Песочница (Проклятая лощина)'
        }
    }
    
    def __init__(self, replay, data):
        self._replay = replay
        self._offset = data['m_timeLocalOffset']
        self._ticks = data['m_timeUTC']
        self._title = data['m_title']
        self._players = self.__createPlayers( data['m_playerList'] )
    
    """
    Метод создает экземпляр на основе данных из Details
    
    @param {dict} playerData данные игрока из реплея
    @param {Team} teamA 
    @param {Team} teamB 
    
    """
    def __createPlayer(self, playerData, teamA, teamB):
        p = Player( 
            self.getReplay(),
            playerData, 
            Toon.getInstance( playerData['m_toon'] ),
            Color( playerData['m_color'] )
        )
        
        if playerData['m_teamId'] == teamA.getId():
            p.setTeam(teamA)
        elif playerData['m_teamId'] == teamB.getId():
            p.setTeam(teamB)
        else:
            raise Exception('несовпадение id предоставленных экземпляров команд с данными игроков')
        return p
    
    """
    за один вызов установит флаг победы для команды
    """
    def __setWinnerTeam(self, playerData, team):
        if playerData['m_teamId'] == team.getId():
            team.setWin( playerData['m_result'] )
        else:
            team.setWin( not playerData['m_result'] )
    
    """
    Создает список `Player` по данным реплея
    """
    def __createPlayers(self, playerDataList):
        teamA, teamB = Team.getPair()
        players = list( 
            map( 
                lambda data: self.__createPlayer(data, teamA, teamB) 
              , playerDataList
            ) 
        )
        self.__setWinnerTeam( playerDataList[0], teamA )
        return players
    
    def getTitle(self):
        return self._title
    
    def getPlayers(self):
        return self._players
        
    def getTeam(self, id):
        team = self._players[0].getTeam()
        if team.id() == id:
            return team
        else: 
            return team.getOppositeTeam()
        
    def getTeams(self):
        team = self._players[0].getTeam()
        return [team, team.getOppositeTeam()]
    
    def getTicks(self):
        return self._ticks
        
    def getOffset(self):
        return self._offset
    
    def getToonIds(self):
        a, b = self.teams()
        ids = a.toondIds()
        print( b.toondIds() )
        # объединение массивов
        ids[len(ids):] = b.toondIds()
        return ids
        
    def getHeroes(self):
        a, b = self.teams()
        heroes = a.heroes()
        # объединение массивов
        heroes[len(heroes):] = b.heroes()
        return heroes
    
    def getNames(self):
        a, b = self.teams()
        names = a.playerNames()
        # объединение массивов
        names[len(names):] = b.playerNames()
        return names
        
    def getDatetime(self):
        return dt.fromtimestamp( winTicksToUnixTime( self.getTicks() ) )
        
        
    def getReplay(self):
        return self._replay
        
    def setReplay(self, replay):
        if self._replay:
            raise Exception('объект `Replay` уже установлен')
            
        self._replay = replay

