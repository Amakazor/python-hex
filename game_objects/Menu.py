from __future__ import annotations

from game_objects.MenuLayer import MenuLayer
from game_objects.TextButton import TextButton
from gamestate.Gamestates import Gamestates
from messaging.MessageBus import MessageBus
from messaging.MessageType import MessageType
from messaging.data.ChangeGamestateData import ChangeGamestateData
from messaging.data.ResizedData import ResizedData
from rendering.IResizeable import IResizeable


class Menu(IResizeable):
    _structure: dict[MenuLayer, list[TextButton]]
    _current_layer: MenuLayer

    def __init__(self, offset: tuple[float, float], screen_size: tuple[float, float]):
        IResizeable.__init__(self)

        self._structure = {}
        self._current_layer = MenuLayer.START
        self._structure[MenuLayer.START] = [
            TextButton(0, 0, offset, screen_size, "Start game", 0.075, lambda sender: self._start_game()),
            TextButton(0, int(screen_size[1] * 0.5), offset, screen_size, "Quit game", 0.075, lambda sender: self._quit_game())
        ]

    def on_resize(self, ticker: object, resize_data: ResizedData):
        for text in self._structure[self._current_layer]:
            text.__del__()

        self._structure[MenuLayer.START] = [
            TextButton(0, 0, resize_data.offset, resize_data.screen_size, "Start game", 0.075, lambda sender: self._start_game()),
            TextButton(0, int(resize_data.screen_size[1] * 0.5), resize_data.offset, resize_data.screen_size, "Quit game",0.075, lambda sender: self._quit_game())
        ]

    def __del__(self):
        IResizeable.__del__(self)
        for text in self._structure[self._current_layer]:
            text.__del__()

    def _start_game(self):
        MessageBus.instance().message(MessageType.CHANGE_GAMESTATE, self, ChangeGamestateData(Gamestates.STARTED))

    def _quit_game(self):
        MessageBus.instance().message(MessageType.CHANGE_GAMESTATE, self, ChangeGamestateData(Gamestates.QUIT))