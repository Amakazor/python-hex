from messaging.data.MessageData import MessageData


class TickData(MessageData):
    _delta_time: float

    @property
    def delta_time(self):
        return self._delta_time

    def __init__(self, delta_time: float):
        self._delta_time = delta_time
