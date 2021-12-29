from __future__ import annotations

from game_objects.MenuLayer import MenuLayer
from game_objects.Text import Text
from game_objects.TextButton import TextButton
from gamestate.Gamestates import Gamestates
from messaging.MessageBus import MessageBus
from messaging.MessageType import MessageType
from messaging.data.ChangeGamestateData import ChangeGamestateData
from messaging.data.ResizedData import ResizedData
from rendering.IResizeable import IResizeable


class Endscreen(IResizeable):
    _structure: list[TextButton | Text]
    _won_player_name: str

    def __init__(self, offset: tuple[float, float], screen_size: tuple[float, float], won_player_name):
        IResizeable.__init__(self)

        self._won_player_name = won_player_name

        self._structure = [
            Text(0, 0, offset, screen_size, self._won_player_name + " won!", 0.075),
            TextButton(0, int(screen_size[1] * 0.5), offset, screen_size, "Main Menu", 0.075, lambda sender: self._quit_game())
        ]

    def on_resize(self, ticker: object, resize_data: ResizedData):
        for text in self._structure:
            text.__del__()

        self._structure = [
            Text(0, 0, resize_data.offset, resize_data.screen_size, self._won_player_name + " won!", 0.075),
            TextButton(0, int(resize_data.screen_size[1] * 0.5), resize_data.offset, resize_data.screen_size, "Quit game", 0.075, lambda sender: self._quit_game())
        ]

    def __del__(self):
        IResizeable.__del__(self)
        for text in self._structure:
            text.__del__()

    def _quit_game(self):
        MessageBus.instance().message(MessageType.CHANGE_GAMESTATE, self, ChangeGamestateData(Gamestates.MENU))
