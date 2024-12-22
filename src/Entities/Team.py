class Team:
    A = 0
    B = 1 
    WIN = 1
    LOSE = 2
    
    @staticmethod
    def getInstance():
        raise Exception('нет необходимости в соблюдении уникальности объекта')
    
    @staticmethod
    def getPair():
        a = Team(Team.A)
        b = Team(Team.B)
        a.setOppositeTeam(b)
        return a, b
    
    def __init__(self, id):
        self._id = id
        self._players = []
        self._win = 0
        self._oppositeTeam = None
        
    def getId(self):
        return self._id
    
    def getWin(self):
        return self._win
        
    def setWin(self, f_win, reciprocal = True):
        self._win = f_win    
        # для установки флага противположной команды с предотвращением цикличности
        if reciprocal:
            self._oppositeTeam.setWin(not f_win, False)
    
    def isWon(self):
        if self._win == 0:
            raise Exception('Значение победы команды не было установлено') 
        return  bool( self._win - 1 ) 
    
    # реализовывать отвязывания не нужно, команды существуют 
    # объект будет создаваться, заполняться и уничтожаться после отработки сразу
    # setter, getter
    def setOppositeTeam(self, team):
        # защита от цекличной перезаписи, когда будет встречно вызвано на противоположном объекте
        if team is self._oppositeTeam:
            return
        
        # так как повторно связывать не придется, но контролировать попытку перезаписи следует
        if self._oppositeTeam != None:
            raise Exception('перезапись отношения')
        
        # инициализация значением
        self._oppositeTeam = team        
        # связывание
        team.setOppositeTeam(self)
    
    def getOppositeTeam(self):
        return self._oppositeTeam  
    
    def getPlayers(self):
        return self._players
    
    def getPlayerNames(self):
        return list( map( lambda p: p.getName() , self.getPlayers() ) )
    
    def getToonIds(self):
        return list( map( lambda p: p.getToon().getId() , self.getPlayers() ) )
        
    def getHeroes(self):
        return list( map( lambda p: p.getHero() , self.getPlayers() ) )
        
    def hasPlayer(self, player):
        pass
    
    def addPlayer(self, player, reciprocal = True):
        if not player:
            return
            
        if len(self._players) >= 5:
            raise Exception('больше 5 игроков в команде')
        
        self._players.append(player)
        
        if reciprocal:
            player.setTeam(self, False)

