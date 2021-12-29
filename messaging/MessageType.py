from enum import Enum


class MessageType(Enum):
    TICK = 1
    RESIZED = 2
    MOUSEMOVED = 3
    MOUSECLICKED = 4
    FIELDSTATECHANGED = 5
    MOVEFINISHED = 6
    RENDER = 7
    CHANGE_GAMESTATE = 8
