from messaging.data.MessageData import MessageData


class MouseClickedData(MessageData):
    _position: tuple[int, int]
    _first_turn: bool

    @property
    def position (self):
        return self._position

    @property
    def first_turn(self):
        return self._first_turn

    def __init__(self, position: tuple[int, int], first_turn: bool):
        self._position = position
        self._first_turn = first_turn
