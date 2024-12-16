import re
from .Realm import Realm
from .Region import Region

class Toon:
    __fields__ = [
        "m_id"
      , "m_programId"
      , "m_realm"
      , "m_region"
    ]
    
    # контейнер уникальных экземпляров полученных через getInstance
    _toons = {}
    
    # Для соблюдения уникальности
    @staticmethod
    def getInstance(replayFormatedData):
        key = Toon._toString(replayFormatedData)
        if key not in Toon._toons:
            try:
                Toon._toons[key] = Toon(replayFormatedData)  
            except ValueError as err:
                return None
        return Toon._toons[key]
    
    @staticmethod
    def parse(rawToon):
        match = re.match(r"""^   
            (?P<region>\d+)-
            (?P<programId>[a-zA-Z]+)-
            (?P<realm>\d+)-
            (?P<id>\d+) 
        $""", rawToon, re.X)
        
        if not match:
            return None
        
        formatedData = Toon.formatAsReplayData(
            match.group('programId')
          , match.group('id')
          , match.group('region')
          , match.group('realm')
        ) 
        return Toon.getInstance( formatedData )
    
    @staticmethod
    def formatAsReplayData(pid, id, region, realm):
        return {
            "m_programId": pid
          , "m_id": id
          , "m_region": region
          , "m_realm": realm
        }
    
    @staticmethod
    def _toString(data):
        return '-'.join(map(lambda v: str(v), [
            data["m_region"],
            data["m_programId"],
            data["m_realm"],
            data["m_id"]
        ]) )
    
    def toString(self):
        return Toon._toString( Toon.formatAsReplayData(
            self.getProgramId(),
            self.getId(),
            self.getRegion().value,
            self.getRealm().value
        ) )

    
    def __init__(self, data):
        self._account = None
        self._players = []
        self._id = data["m_id"]
        self._realm = Realm( int( data["m_realm"] ) )
        self._region = Region( int( data["m_region"] ) )
        self._programId = data["m_programId"]
                
    def getId(self):
        return self._id
    
    def getRealm(self):
        return self._realm
    
    def getRegion(self):
        return self._region
        
    def getProgramId(self):
        return self._programId
    
    def getPlayers():
        return self._players
    
    def addPlayer(self, player, reciprocal = True):
        self._players.append( player )
        
        if reciprocal:
            player.setToon(self, False)
    
    def setAccount(self, account, reciprocal = True):
        if self._account:
            raise Exception('аккаунт уже установлен для текущего ')
        
        self._account = account
        
        if reciprocal:
            account.addToon(self, False)
        
    def getAccount(self):
        return self._account
    