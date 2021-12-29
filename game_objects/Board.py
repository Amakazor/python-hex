from __future__ import annotations

from game_objects.Field import Field
from game_objects.Player import Player
from messaging.MessageBus import MessageBus
from messaging.MessageType import MessageType


class Board:
    _fields: list[list[Field]]
    _players: list[Player]

    _current_player: int

    @property
    def fields(self):
        return self._fields

    @property
    def current_player(self):
        return self._players[self._current_player]

    def __init__(self, players: list[Player], offset: tuple[float, float], screen_size: tuple[float, float]) -> None:
        self._players = players
        self._current_player = 0

        self.generate_fields(offset, screen_size)
        self.generate_neighbors()

        MessageBus.instance().register(MessageType.RESIZED, lambda sender, data: self.recalculate(data.offset, data.screen_size))

    def __del__(self):
        for y in range(12):
            for x in range(12):
                self._fields[y][x].__del__()

    def generate_fields(self, offset: tuple[float, float], screen_size: tuple[float, float]) -> None:
        self._fields = []
        for y in range(12):
            row = []
            for x in range(12):
                row.append(Field(y, x, self, offset, screen_size))
            self._fields.append(row)

    def generate_neighbors(self) -> None:
        for y in range(12):
            for x in range(12):
                neighbors: list[Field] = []
                for neighborY in range(-1, 2):
                    for neighborX in range(-1, 2):
                        if (neighborY != 0 or neighborX != 0) and not (neighborY != 0 and neighborX != 0) and (y + neighborY != -1 and y + neighborY != 12) and (x + neighborX != -1 and x + neighborX != 12):
                            neighbors.append(self._fields[y + neighborY][x + neighborX])
                if y + 1 != -1 and y + 1 != 12 and x - 1 != -1 and x - 1 != 12:
                    neighbors.append(self._fields[y + 1][x - 1])
                if y - 1 != -1 and y - 1 != 12 and x + 1 != -1 and x + 1 != 12:
                    neighbors.append(self._fields[y - 1][x + 1])
                self._fields[y][x].add_neighbors(neighbors)

    def get_field_at_coordinates(self, x: int, y: int) -> Field:
        if 0 < x < 12 and 0 < y < 12:
            return self._fields[y][x]
        else:
            raise AttributeError("x and y need to be in range from 0 to 12")

    def recalculate(self, offset: tuple[float, float], screen_size: tuple[float, float]) -> None:
        for y in range(12):
            for x in range(12):
                self._fields[x][y].recalculate(offset, screen_size)

    def change_player(self) -> None:
        self._current_player = 1 if self._current_player == 0 else 0

    def check_for_win(self, last_field: Field) -> Player | None:
        found_first = False
        found_last = False

        closed_fields: set[Field] = set()
        open_fields: set[Field] = {last_field}

        while len(open_fields) > 0:
            for field in open_fields.copy():
                open_fields.remove(field)
                for neighbor in field.neighbors:
                    if neighbor not in closed_fields and neighbor.player == self.current_player:
                        open_fields.add(neighbor)

                if self._current_player == 0:
                    if field.x == 0:
                        found_first = True
                    elif field.x == 11:
                        found_last = True
                else:
                    if field.y == 0:
                        found_first = True
                    elif field.y == 11:
                        found_last = True

                if found_first and found_last:
                    return self._players[self._current_player]

                closed_fields.add(field)

        return None
