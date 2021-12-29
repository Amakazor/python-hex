from __future__ import annotations

from pygame import Color

import Engine
from game_objects.Endscreen import Endscreen
from game_objects.Board import Board
from game_objects.Menu import Menu
from game_objects.Player import Player
from gamestate.Gamestates import Gamestates
from messaging.data.ChangeGamestateData import ChangeGamestateData
from messaging.data.FieldStateChangedData import FieldStateChangedData
from messaging.MessageBus import MessageBus
from messaging.MessageType import MessageType


class Gamestate:
    _currentState: Gamestates
    _board: Board | None
    _engine: Engine.Engine
    _won_player: Player | None
    _menu: Menu | None
    _endscreen: Endscreen | None

    def __init__(self, engine: Engine.Engine):
        self._currentState = Gamestates.MENU
        self._engine = engine
        self._won_player = None

        MessageBus.instance().register(MessageType.FIELDSTATECHANGED, self._on_field_state_change)
        MessageBus.instance().register(MessageType.MOVEFINISHED, self._on_move_finished)

        MessageBus.instance().register(MessageType.CHANGE_GAMESTATE, lambda sender, data: self._on_gamestate_change(sender, data))

        self._enter_menu()

    @property
    def current_state(self):
        return self._currentState

    @current_state.setter
    def current_state(self, value: Gamestates):
        if value == Gamestates.STARTED:
            self._start_game()
            self._currentState = Gamestates.STARTED
        if value == Gamestates.QUIT:
            self._engine.quit()
            self._currentState = Gamestates.QUIT
        if value == Gamestates.FINISHED:
            self._finish_game()
            self._enter_endscreen()
            self._currentState = Gamestates.FINISHED
        if value == Gamestates.MENU:
            self._finish_game()
            self._enter_menu()
            self._currentState = Gamestates.MENU

    def _on_gamestate_change(self, sender: object, data: ChangeGamestateData):
        self.current_state = data.gamestate

    def _enter_menu(self):
        if self._currentState == Gamestates.FINISHED:
            self._endscreen.__del__()
            self._endscreen = None

            self._won_player = None

        self._menu = Menu(self._engine.letterbox, (self._engine.board_height, self._engine.board_width))

    def _enter_endscreen(self):
        self._endscreen = Endscreen(self._engine.letterbox, (self._engine.board_height, self._engine.board_width), self._won_player.name)

    def _start_game(self):
        if self._currentState == Gamestates.MENU:
            self._menu.__del__()
            self._menu = None

            self._won_player = None

            player1 = Player("Player 1", Color(255, 50, 50))
            player2 = Player("Player 2", Color(50, 50, 255))
            self._board = Board([player1, player2], self._engine.letterbox, (self._engine.board_height,
                                                                             self._engine.board_width))

    def _finish_game(self):
        if self._currentState == Gamestates.STARTED:
            self._board.__del__()
            self._board = None

    def _on_field_state_change(self, sender: object, data: FieldStateChangedData):
        if self._currentState == Gamestates.STARTED:
            won_player = self._board.check_for_win(data.field)
            if won_player is not None:
                self._won_player = won_player
                self.current_state = Gamestates.FINISHED

    def _on_move_finished(self, sender: object, data: None):
        if self._currentState == Gamestates.STARTED:
            self._board.change_player()
