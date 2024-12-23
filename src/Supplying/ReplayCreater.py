from ..Config import Config
from ..Entities import Replay

import src.conditions as conditions

class ReplayCreater:
    def __init__(self, extracter):
        self._extracter = extracter
        
    def create(self, path):
        if not conditions.isReplaySource(path):
            return None
        return Replay.getInstance( path, self._extracter )        
    
    