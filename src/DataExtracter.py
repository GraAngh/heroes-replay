from subprocess import Popen, PIPE
import json

class DataExtracter:
    HEADER = 'header'
    DETAILS = 'details'
    STATS = 'stats'
    INIT_DATA = 'initdata'
    ATTR_EVENTS = 'attributeevents'
    GAME_EVENTS = 'gameevents'
    TRACKER_EVENTS = 'trackerevents'
    MESSAGE_EVENTS = 'messageevents' 
        
    def __init__(self, cacher):
        self._cacher = cacher
    
    def _extract(self, replayFile, arg):
        p1 = Popen(["python", "-m", "heroprotocol", "--json", "--" + arg, replayFile], stdout = PIPE)
        data = p1.stdout.read()
        data = data.decode('utf-8')
        if len(data):
            return json.loads( data )        
        return None
    
    def _getterTemplate(self, file, arg):
        data = self._cacher.read(file, arg)
        if not data:
            data = self._extract(file, arg)
            self._cacher.write(file, arg, data)
        if data:
            return data
        return None
    
    def getDetails(self, file):
        return self._getterTemplate(file, self.DETAILS)
     
    def getInitData(self, file):
        return None
        
    def getHeader(self, file):
        return None
        
    def getAttributeEvents(self, file):
        return None
        
    def getGameEvents(self, file):
        return None
        
    def getMessageEvents(self, file):
        return None
        
    def getTrackerEvents(self, file):
        return None