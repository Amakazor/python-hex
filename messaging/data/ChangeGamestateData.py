from gamestate.Gamestates import Gamestates
from messaging.data.MessageData import MessageData


class ChangeGamestateData(MessageData):
    _gamestate: Gamestates

    @property
    def gamestate(self):
        return self._gamestate

    def __init__(self, gamestate: Gamestates):
        self._gamestate = gamestate
