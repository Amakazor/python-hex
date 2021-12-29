from __future__ import annotations

from pygame import Color, Surface

from rendering.RenderLayer import RenderLayer
from rendering.RenderType import RenderType


class RenderBuffer:
    _buffer: list[list[tuple[RenderType, tuple[Color, list[tuple[float, float]]] | tuple[tuple[float, float], Surface]]]]

    @property
    def buffer(self):
        return self._buffer

    def __init__(self):
        self._buffer = []
        for layer in RenderLayer:
            self._buffer.append([])

    def add_polygon(self, render_layer: int, color: Color, points: list[tuple[float, float]]):
        self._buffer[render_layer].append((RenderType.POLYGON, (color, points)))

    def add_surface(self, render_layer: int, position: tuple[float, float], surface: Surface):
        self._buffer[render_layer].append((RenderType.SURFACE, (position, surface)))
