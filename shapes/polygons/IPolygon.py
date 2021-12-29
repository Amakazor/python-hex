from abc import ABC, abstractmethod


class IPolygon(ABC):

    @abstractmethod
    def points(self):
        pass

    @abstractmethod
    def is_inside(self, point: tuple[float, float]):
        pass
