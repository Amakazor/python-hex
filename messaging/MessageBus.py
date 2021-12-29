from __future__ import annotations
from typing import Callable
from messaging.MessageType import MessageType
from messaging.data.MessageData import MessageData


class MessageBus:
    _instance: None | MessageBus = None
    _handlers: dict[MessageType, set[Callable[[object, MessageData], None]]] = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def register(self, message_type: MessageType, handler: Callable[[object, MessageData], None]):
        if message_type not in self._handlers:
            self._handlers[message_type] = {handler}
        else:
            self._handlers[message_type].add(handler)

    def unregister(self, message_type: MessageType, handler: Callable[[object, MessageData], None]):
        if message_type in self._handlers and handler in self._handlers[message_type]:
            self._handlers[message_type].remove(handler)

    def message(self, message_type: MessageType, sender: object, message_data: MessageData):
        if message_type in self._handlers:
            for handler in self._handlers[message_type].copy():
                handler(sender, message_data)
