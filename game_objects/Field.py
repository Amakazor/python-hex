from __future__ import annotations

from pygame.color import Color

from game_objects import Board
from interactivity.IMouseable import IMouseable
from interactivity.ITickable import ITickable
from messaging.data import FieldStateChangedData
from messaging.data.RenderData import RenderData
from messaging.MessageBus import MessageBus
from messaging.MessageType import MessageType
from messaging.data.MouseClickedData import MouseClickedData
from messaging.data.MouseMovedData import MouseMovedData
from messaging.data.TickData import TickData
from game_objects.Player import Player
from shapes.polygons.Hexagon import Hexagon
from rendering.IRenderable import IRenderable
from rendering.RenderLayer import RenderLayer


class Field(ITickable, IRenderable, IMouseable):
    _x: int
    _y: int

    _board: Board.Board

    _neighbors: list[Field]

    _player: Player | None

    _polygon: Hexagon
    _center_polygon: Hexagon

    _offsets: tuple[float, float]
    _screen_size: tuple[float, float]

    _hovered: bool
    _neighbor_hovered: bool

    _hovered_mask: float
    _hovered_value: float
    _neighbor_hovered_value: float

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def neighbors(self):
        return self._neighbors

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, new_player: Player):
        self._player = new_player

    @property
    def hovered(self):
        return self._hovered

    @hovered.setter
    def hovered(self, value):
        for neighbor in self._neighbors:
            if self._player is None:
                neighbor.neighbor_hovered = value
            else:
                neighbor.neighbor_hovered = False
        self._hovered = value

    @property
    def neighbor_hovered(self):
        return self._neighbor_hovered

    @neighbor_hovered.setter
    def neighbor_hovered(self, value):
        self._neighbor_hovered = value
        if self.player is not None:
            for neighbor in self._neighbors:
                if neighbor.player is self._player and neighbor._neighbor_hovered is not value:
                    neighbor.neighbor_hovered = value

    def __init__(self, x: int, y: int, board: Board.Board, offset: tuple[float, float], screen_size: tuple[float, float]):
        ITickable.__init__(self)
        IRenderable.__init__(self)
        IMouseable.__init__(self)

        self._x = x
        self._y = y

        self._board = board

        self._player = None

        self._neighbors = []

        self._hovered = False
        self._neighbor_hovered = False

        self._hovered_mask = 1

        self._hovered_value = 0.6
        self._neighbor_hovered_value = 0.75

        self.recalculate(offset, screen_size, True)

    def __del__(self):
        ITickable.__del__(self)
        IRenderable.__del__(self)
        IMouseable.__del__(self)

    def add_neighbors(self, neighbors: list[Field]):
        self._neighbors = neighbors

    def recalculate(self, offset: tuple[float, float], screen_size: tuple[float, float], force: bool = False):
        if force or offset is not self._offsets or screen_size is not self._screen_size:
            self._offsets = offset
            self._screen_size = screen_size

            size = screen_size[0] / 11
            offset = (self._offsets[0] + size / 2, self._offsets[1] + size / 2)

            self._polygon = Hexagon((
                (self.x + 0.5 * self.y) * size + offset[0],
                self.y * size * 0.9 + offset[1]
            ), size * 0.5)
            self._center_polygon = Hexagon((
                (self.x + 0.5 * self.y) * size + offset[0],
                self.y * size * 0.9 + offset[1]
            ), size * 0.45)

    def on_render(self, ticker: object, render_data: RenderData):
        buffer = render_data.buffer
        buffer.add_polygon(RenderLayer.FOREGROUND.value, Color(255, 255, 255) if self._player is None else self._player.color, self._polygon.points)

        if self._player is not None:
            buffer.add_polygon(RenderLayer.FOREGROUND.value, Color(int(self._hovered_mask * self._player.color.r), int(self._hovered_mask * self._player.color.g), int(self._hovered_mask * self._player.color.b)), self._center_polygon.points)

        if self._player is None:
            buffer.add_polygon(RenderLayer.FOREGROUND.value, Color(int(self._hovered_mask * 255), int(self._hovered_mask * 255), int(self._hovered_mask * 255)), self._center_polygon.points)

    def is_inside(self, point: tuple[float, float]):
        return self._polygon.is_inside(point)

    def tick(self, ticker, tick_data: TickData):
        delta_time = tick_data.delta_time
        animation_speed_multiplier = 4
        hovered_animation_speed_multiplier = animation_speed_multiplier * (1 - self._hovered_value)
        neighbor_hovered_animation_speed_multiplier = animation_speed_multiplier * (1 - self._neighbor_hovered_value)

        if (not self._hovered or self.player is not None) and (not self._neighbor_hovered or (self.player is not self._board.current_player and self.player is not None)) and self._hovered_mask < 1:
            self._hovered_mask = min(1, self._hovered_mask + delta_time)

        if self._hovered and self._player is None:
            if self._hovered_mask > self._hovered_value:
                self._hovered_mask = max(self._hovered_value,
                                         self._hovered_mask - delta_time * hovered_animation_speed_multiplier)
            elif self._hovered_mask < self._hovered_value:
                self._hovered_mask = min(self._hovered_value,
                                         self._hovered_mask + delta_time * hovered_animation_speed_multiplier)

        if self._neighbor_hovered and (self._player is None or self._player is self._board.current_player):
            if self._hovered_mask > self._neighbor_hovered_value:
                self._hovered_mask = max(self._neighbor_hovered_value,
                                         self._hovered_mask - delta_time * neighbor_hovered_animation_speed_multiplier)
            elif self._hovered_mask < self._neighbor_hovered_value:
                self._hovered_mask = min(self._neighbor_hovered_value,
                                         self._hovered_mask + delta_time * neighbor_hovered_animation_speed_multiplier)

    def on_mouse_click(self, mouse_clicker: object, data: MouseClickedData):
        if (self._player is None or data.first_turn) and self.is_inside(data.position):
            self.player = self._board.current_player
            self.hovered = self.hovered
            MessageBus.instance().message(MessageType.FIELDSTATECHANGED, self, FieldStateChangedData.FieldStateChangedData(self))
            MessageBus.instance().message(MessageType.MOVEFINISHED, self, None)

    def on_mouse_move(self, mouse_mover: object, data: MouseMovedData):
        if not self._hovered and self.is_inside(data.position):
            self.hovered = True
        elif self._hovered and not self.is_inside(data.position):
            self.hovered = False
