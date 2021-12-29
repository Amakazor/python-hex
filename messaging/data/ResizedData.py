from messaging.data.MessageData import MessageData


class ResizedData(MessageData):
    _offset: tuple[float, float]
    _screen_size: tuple[float, float]
    _raw_screen_size: tuple[float, float]

    @property
    def offset(self):
        return self._offset

    @property
    def screen_size(self):
        return self._screen_size

    @property
    def raw_screen_size(self):
        return self._raw_screen_size

    def __init__(self, offset: tuple[float, float], screen_size: tuple[float, float], raw_screen_size: tuple[float, float]):
        self._offset = offset
        self._screen_size = screen_size
        self._raw_screen_size = raw_screen_size
