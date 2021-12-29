from math import cos, pi, sin, sqrt

from shapes.polygons.IPolygon import IPolygon


class Hexagon(IPolygon):
    _center: tuple[float, float]
    _radius: float

    _points: list[tuple[float, float]]

    @property
    def center(self):
        return self._center

    @property
    def radius(self):
        return self._radius

    @property
    def points(self):
        return self._points

    def __init__(self, center: tuple[float, float], radius: float):
        self._center = center
        self._radius = radius

        self.calculate_points()

    def calculate_points(self):
        self._points = [(
                self._center[0] + self._radius * sin(2 * pi * i / 6),
                self._center[1] + self._radius * cos(2 * pi * i / 6)
            )
            for i in range(6)
        ]

    def is_inside(self, point: tuple[float, float]):
        abs_point = (abs(point[0] - self._center[0]), abs(point[1] - self._center[1]))

        vertical = self._radius / 2
        horizontal = self._radius * sqrt(3) / 2

        if abs_point[0] > horizontal or abs_point[1] > vertical * 2:
            return False
        return 2 * vertical * horizontal - vertical * abs_point[0] - horizontal * abs_point[1] >= 0

