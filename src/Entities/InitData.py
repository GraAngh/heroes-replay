class InitData:
    def __init__(self, replay, data):
        self._replay = replay
        self._data = data
        self._gameDescr = self._data['m_syncLobbyState']['m_gameDescription']
        
    def gameDescription(self):
        return self._gameDescr
        

