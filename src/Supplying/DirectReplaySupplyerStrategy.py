from .ReplayCreater import ReplayCreater

class DirectReplaySupplyerStrategy:
    def __init__(self, replayCreater):
        self._creater = replayCreater

    def supply(self, path, cb):
        r = self._creater.create(path)
        if r:
            cb( r )
            