from abc import ABC, abstractmethod

from messaging.MessageBus import MessageBus
from messaging.MessageType import MessageType
from messaging.data.ResizedData import ResizedData


class IResizeable(ABC):

    def __init__(self):
        MessageBus.instance().register(MessageType.RESIZED, self.on_resize)

    def __del__(self):
        MessageBus.instance().unregister(MessageType.RESIZED, self.on_resize)

    @abstractmethod
    def on_resize(self, ticker: object, resize_data: ResizedData):
        pass
