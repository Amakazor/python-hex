from messaging.data.MessageData import MessageData
from rendering.RenderBuffer import RenderBuffer


class RenderData(MessageData):
    _buffer: RenderBuffer

    @property
    def buffer(self):
        return self._buffer

    def __init__(self, buffer: RenderBuffer):
        self._buffer = buffer
