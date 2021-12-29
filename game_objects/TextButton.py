from collections import Callable

from game_objects.Text import Text

from messaging.data.MouseClickedData import MouseClickedData


class TextButton(Text):
    _action: Callable[[object], None]

    def __init__(self, x: int, y: int, offset: tuple[float, float], screen_size: tuple[float, float], text: str, size: float, action: Callable[[object], None]):
        super(TextButton, self).__init__(x, y, offset, screen_size, text, size)

        self._action = action

        self.recalculate(offset, screen_size, True)

    def __del__(self):
        super(TextButton, self).__del__()

    def on_mouse_click(self, mouse_clicker: object, data: MouseClickedData):
        if self.is_inside(data.position):
            self._action(self)
