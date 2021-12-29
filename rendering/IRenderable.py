from abc import ABC, abstractmethod

from messaging.data import RenderData
from messaging.MessageBus import MessageBus
from messaging.MessageType import MessageType


class IRenderable(ABC):

    def __init__(self):
        MessageBus.instance().register(MessageType.RENDER, self.on_render)

    def __del__(self):
        MessageBus.instance().unregister(MessageType.RENDER, self.on_render)

    @abstractmethod
    def on_render(self, ticker: object, render_data: RenderData):
        pass
