from abc import ABC, abstractmethod

from messaging.MessageBus import MessageBus
from messaging.MessageType import MessageType
from messaging.data.MouseMovedData import MouseMovedData
from messaging.data.MouseClickedData import MouseClickedData


class IMouseable(ABC):

    def __init__(self):
        MessageBus.instance().register(MessageType.MOUSECLICKED, self.on_mouse_click)
        MessageBus.instance().register(MessageType.MOUSEMOVED, self.on_mouse_move)

    def __del__(self):
        MessageBus.instance().unregister(MessageType.MOUSECLICKED, self.on_mouse_click)
        MessageBus.instance().unregister(MessageType.MOUSEMOVED, self.on_mouse_move)

    @abstractmethod
    def on_mouse_click(self, mouse_clicker: object, data: MouseClickedData):
        pass

    @abstractmethod
    def on_mouse_move(self, mouse_mover: object, data: MouseMovedData):
        pass
