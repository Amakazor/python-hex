import os
from collections import Callable
from msilib.schema import Font

import pygame
from pygame import Surface

from messaging.data.RenderData import RenderData
from messaging.data.ResizedData import ResizedData
from rendering.IRenderable import IRenderable
from rendering.IResizeable import IResizeable
from rendering.RenderLayer import RenderLayer


class Background(IRenderable, IResizeable):
    _screen_size: tuple[float, float]

    _background: Surface

    def __init__(self, screen_size: tuple[float, float]):
        IRenderable.__init__(self)
        IResizeable.__init__(self)

        self.recalculate(screen_size, True)

    def __del__(self):
        IRenderable.__del__(self)
        IResizeable.__del__(self)

    def on_resize(self, ticker: object, resize_data: ResizedData):
        self.recalculate(resize_data.raw_screen_size)

    def recalculate(self, screen_size: tuple[float, float], force: bool = False):
        if force or screen_size is not self._screen_size:
            self._screen_size = screen_size
            self._background = pygame.transform.scale(pygame.Surface.convert(pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "resources", "wood.png"))), (max(self._screen_size[0], self._screen_size[1]), max(self._screen_size[0], self._screen_size[1])))

    def on_render(self, ticker: object, render_data: RenderData):
        buffer = render_data.buffer
        buffer.add_surface(RenderLayer.BACKGROUND.value, (0, 0), self._background)
