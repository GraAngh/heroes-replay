class UserStateManager(Config):
    USER_STATES_FILE = 'hero-replay_UserStates.json'
    
    def __init__(self):
        self._fileName = file = getenv('TMP') + f'\{self.USER_STATES_FILE}'
        self.__file = self.load()
        self._data = {}
        
    def remove(self, id):
        
    def save(self):
        with open(self._fileName, encodinf='utf-8') as f:
            f.write()
        