from collections import Callable
from msilib.schema import Font

import pygame
from pygame import Surface

from interactivity.IMouseable import IMouseable
from interactivity.ITickable import ITickable
from messaging.data import RenderData
from messaging.data.MouseClickedData import MouseClickedData
from messaging.data.MouseMovedData import MouseMovedData
from messaging.data.ResizedData import ResizedData
from messaging.data.TickData import TickData
from rendering.IRenderable import IRenderable
from rendering.IResizeable import IResizeable
from rendering.RenderLayer import RenderLayer


class Text(ITickable, IRenderable, IMouseable, IResizeable):
    _x: int
    _y: int

    _offsets: tuple[float, float]
    _screen_size: tuple[float, float]

    _font: Font
    _text: str
    _size: float

    _main_text: Surface
    _outline_text: Surface

    def __init__(self, x: int, y: int, offset: tuple[float, float], screen_size: tuple[float, float], text: str, size: float):
        ITickable.__init__(self)
        IRenderable.__init__(self)
        IResizeable.__init__(self)
        IMouseable.__init__(self)

        self._x = x
        self._y = y

        self._text = text
        self._size = size

        self.recalculate(offset, screen_size, True)

    def __del__(self):
        ITickable.__del__(self)
        IRenderable.__del__(self)
        IResizeable.__del__(self)
        IMouseable.__del__(self)

    def on_resize(self, ticker: object, resize_data: ResizedData):
        self.recalculate(resize_data.offset, resize_data.screen_size)

    def recalculate(self, offset: tuple[float, float], screen_size: tuple[float, float], force: bool = False):
        if force or offset is not self._offsets or screen_size is not self._screen_size:
            self._offsets = offset
            self._screen_size = screen_size
            self._font = pygame.font.SysFont("Arial", int(self._screen_size[1] * self._size))

            self._main_text = self._font.render(self._text, True, pygame.Color(0, 0, 0))
            self._outline_text = self._font.render(self._text, True, pygame.Color(255, 255, 255))

    def tick(self, ticker: object, tick_data: TickData):
        pass

    def on_render(self, ticker: object, render_data: RenderData):
        buffer = render_data.buffer

        buffer.add_surface(RenderLayer.TOP.value, (self._offsets[0] - self._screen_size[0] / 40 * self._size + self._x, self._offsets[1] - self._screen_size[0] / 40 * self._size + self._y), self._outline_text)
        buffer.add_surface(RenderLayer.TOP.value, (self._offsets[0] - self._screen_size[0] / 40 * self._size + self._x, self._offsets[1] + self._screen_size[0] / 40 * self._size + self._y), self._outline_text)
        buffer.add_surface(RenderLayer.TOP.value, (self._offsets[0] + self._screen_size[0] / 40 * self._size + self._x, self._offsets[1] + self._screen_size[0] / 40 * self._size + self._y), self._outline_text)
        buffer.add_surface(RenderLayer.TOP.value, (self._offsets[0] + self._screen_size[0] / 40 * self._size + self._x, self._offsets[1] - self._screen_size[0] / 40 * self._size + self._y), self._outline_text)

        buffer.add_surface(RenderLayer.TOP.value, (self._offsets[0] + self._x, self._offsets[1] - self._screen_size[0] / 40 * self._size + self._y), self._outline_text)
        buffer.add_surface(RenderLayer.TOP.value, (self._offsets[0] + self._x, self._offsets[1] + self._screen_size[0] / 40 * self._size + self._y), self._outline_text)
        buffer.add_surface(RenderLayer.TOP.value, (self._offsets[0] + self._screen_size[0] / 40 * self._size + self._x, self._offsets[1] + self._y), self._outline_text)
        buffer.add_surface(RenderLayer.TOP.value, (self._offsets[0] - self._screen_size[0] / 40 * self._size + self._x, self._offsets[1] + self._y), self._outline_text)

        buffer.add_surface(RenderLayer.TOP.value, (self._offsets[0] + self._x, self._offsets[1] + self._y), self._main_text)

    def is_inside(self, point: tuple[float, float]):
        return self._offsets[0] + self._x <= point[0] <= self._main_text.get_width() + self._offsets[0] + self._x and self._offsets[1] + self._y <= point[1] <= self._main_text.get_height() + self._offsets[1] + self._y

    def on_mouse_click(self, mouse_clicker: object, data: MouseClickedData):
        pass

    def on_mouse_move(self, mouse_mover: object, data: MouseMovedData):
        pass