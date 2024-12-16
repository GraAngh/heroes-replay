class Player:
    __fields__ = [
        "m_color"
      , "m_control"
      , "m_handicap"
      , "m_hero"
      , "m_name"
      , "m_observe" # зритель [0,1]
      , "m_race"     # 
      , "m_result"  # литерал победы [1, 2] для (можно перенести в `Team`)
      , "m_teamId"  # литерал id для `Team`
      , "m_toon"    # данные `Toon`
      , "m_workingSetSlotId"
    ]
    
    def __init__(self, replay, data, toon, color, team = None):
        self._name = data['m_name']
        self._hero = data['m_hero']
        self._observer = data['m_observe']
        self._slot = data['m_workingSetSlotId']
        self._replay = replay
        
        self._toon = None
        self._color = None
        self._team = None
        
        self.setTeam(team)
        self.setColor(color)
        self.setToon(toon)
     
    def getName(self):
        return self._name
    
    def getHero(self):
        return self._hero
        
    def isObserver(self):
        return self._observer
        
    def getSlot(self):
        return self._slot
    
    def getTeam(self):
        return self._team
        
    def setTeam(self, t, reciprocal = True):
        # защита от цикличного присванивания
        if not t:
            return
             
        self._team = t
        
        if reciprocal:
            t.addPlayer(self, False)
    
    def isWin(self):
        return self._team.isWin()
    
    def getToon(self):
        return self._toon
    
    def setToon(self, toon, reciprocal = True):
        if toon is self._toon:
            return
    
        if self._toon:
            raise Exception('Уникальное изображение игрока уже установлено')
        
        self._toon = toon
        
        if reciprocal:
            toon.addPlayer(self, False)
        
    def setColor(self, color):
        self._color = color
    
    def getColor(self):
        return self._color

    def toString(self):
        name = self.getName()
        hero = self.getHero()
        toon = self.getToon()
        if toon:            
            region = toon.getRegion().name
            realm = toon.getRealm().name
            toonId = toon.getId()
            return f'{toonId:<8}  {name:<12} `{hero:^8}` ({region}-{realm})'
            
        return f'{name:<12} {hero:<8} (NAN)'  