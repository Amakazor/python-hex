from messaging.data.MessageData import MessageData


class MouseClickedData(MessageData):
    _position: tuple[int, int]

    @property
    def position (self):
        return self._position

    def __init__(self, position: tuple[int, int]):
        self._position = position
