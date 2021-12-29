from messaging.data.MessageData import MessageData


class FieldStateChangedData(MessageData):
    _field = None

    @property
    def field(self):
        return self._field

    def __init__(self, field):
        self._field = field
