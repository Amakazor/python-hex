from abc import ABC, abstractmethod

from messaging.MessageBus import MessageBus
from messaging.MessageType import MessageType
from messaging.data.TickData import TickData


class ITickable(ABC):

    def __init__(self):
        MessageBus.instance().register(MessageType.TICK, self.tick)

    def __del__(self):
        MessageBus.instance().unregister(MessageType.TICK, self.tick)

    @abstractmethod
    def tick(self, ticker: object, tick_data: TickData):
        pass
