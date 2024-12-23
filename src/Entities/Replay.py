import os
from hashlib import sha256
from .Details import Details
from .InitData import InitData
from .Header import Header
from .AttributeEvents import AttributeEvents
from .MessageEvents import MessageEvents
from .TrackerEvents import TrackerEvents
from .GameEvents import GameEvents


class Replay:
    __replayes = {}
    
    @staticmethod
    def getInstance(path, extracter):
        r = Replay(path, extracter)
        date  = r.getDate() 
        title = r.getTitle()
        id = sha256( f'{title}_{date}'.encode('utf-8') ).hexdigest()
 
        if id in Replay.__replayes:
            return Replay.__replayes[id]
        if not r.isRelevant():
            return None
        Replay.__replayes[id] = r
        return r
    
    """
    @param extracter {Extracter} класс получения конкертных данных из исходного 
        файла реплея. Он конфигурируется на старте и доступен через родительский
        класс программы, который доступен черз объект-синглетон Config

    """
    def __init__(self, path, extracter):
        self._path = path
        self._extracter = extracter
        self._details = None
        self._initData = None
        self._header = None
        self._attributeEvents = None
        self._gameEvents = None
        self._messageEvents = None
        self._trackerEvents = None
    
    def getPath(self):
        return self._path
    
    def getName(self):
        base = os.path.basename( self.getPath() )
        name, ext = os.path.splitext( base )
        return name
    
    def getPlayers(self):
        return self.getDetails().getPlayers()
    
    def getTeams(self):
        return self.getDetails().getTeams()
    
    def getDate(self):
        return self.getDetails().getDatetime().isoformat(' ')
    
    def getTitle(self):
        return self.getDetails().getTitle()
    
    # КОмпозиционные части
    def getDetails(self):
        if not self._details:
            data = self._extracter.getDetails(self._path)
            if data:
                self._details = Details(self, data)
        return self._details
     
    def getInitData(self):
        if not self._initData:
            data = self._extracter.getInitData(self._path)
            if data:
                self._initData = InitData(self, data)
        return self._initData
        
    def getHeader(self):
        if not self._header:
            data = self._extracter.getHeader(self._path)
            if data:
                self._header = Header(self, data)
        return self._header
        
    def getAttributeEvents(self):
        if not self._attributeEvents:
            data = self._extracter.getAttributeEvents(self._path)
            if data:
                self._attributeEvents = AttributeEvents(self, data)
        return self._attributeEvents
        
    def getGameEvents(self):
        if not self._gameEvents:
            data = self._extracter.getGameEvents(self._path)
            if data:
                self._gameEvents = GameEvents(self, data)
        return self._gameEvents
        
    def getMessageEvents(self):
        if not self._messageEvents:
            data = self._extracter.getMessageEvents(self._path)
            if data:
                self._messageEvents = MessageEvents(self, data)
        return self._messageEvents
        
    def getTrackerEvents(self):
        if not self._trackerEvents:
            data = self._extracter.getTrackerEvents(self._path)
            if data:
                self._trackerEvents = TrackerEvents(self, data)
        return self._trackerEvents
        
    def isRelevant(self):
        # Это уже реальная проверка файла 
        try:
            self.getHeader()
            return True
        except:
            return False