from ..Config import Config
from ..Entities import Replay

import src.conditions as conditions

class ReplayCreater:
    def __init__(self, extracter):
        self._extracter = extracter
        
    def create(self, path):
        # это внешняя проверка, не гарантирующая, что файл является реплеем.
        # Т.е. прредположим, что внутри данные реплея
        if not conditions.isReplaySource(path):
            return None
        return Replay.getInstance( path, self._extracter )        
    
    