from __future__ import annotations
from pygame import Color


class Player:
    _name: str
    _color: Color

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    def __init__(self, name: str, color: Color):
        self._name = name
        self._color = color
