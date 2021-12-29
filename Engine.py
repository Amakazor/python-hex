import pygame
import pygame.gfxdraw
from pygame.surface import Surface

from game_objects.Background import Background
from gamestate.Gamestates import Gamestates
from messaging.MessageBus import MessageBus
from messaging.MessageType import MessageType
from messaging.data.MouseClickedData import MouseClickedData
from messaging.data.MouseMovedData import MouseMovedData
from messaging.data.RenderData import RenderData
from messaging.data.ResizedData import ResizedData
from messaging.data.TickData import TickData
from gamestate.Gamestate import Gamestate
from rendering.RenderBuffer import RenderBuffer
from rendering.RenderType import RenderType


class Engine:
    _aspect_ratio: float
    _width: float
    _height: float

    _margin_base: float
    _margin: float
    _letterbox: (float, float)

    _quit: bool
    _screen: Surface

    _background: Background

    _gamestate: Gamestate

    @property
    def letterbox(self):
        return self._letterbox

    @property
    def board_width(self):
        return self._width - 2 * self._margin

    @property
    def board_height(self):
        return self._height - 2 * self._margin

    def __init__(self):
        self._aspect_ratio = 1.5
        self._height = 600
        self._width = self._height * self._aspect_ratio

        self._margin_base = 0.1
        self._margin = self._margin_base * min(self._width, self._height)
        self._letterbox = (self._margin, self._margin)

        pygame.init()

        self._screen = pygame.display.set_mode((self._width, self._height), pygame.RESIZABLE)
        self._gamestate = Gamestate(self)
        self._quit = False

        self._background = Background((self._width, self._height))

    def start(self):
        last_frame_ticks = pygame.time.get_ticks()

        while not self._quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit = True
                elif event.type == pygame.VIDEORESIZE:
                    self._width = event.w
                    self._height = event.h
                    self._margin = self._margin_base * min(self._width, self._height)

                    if self._width > self._height * self._aspect_ratio:
                        self._letterbox = ((self._width - (self._height * self._aspect_ratio)) / 2 + self._margin, self._margin)
                        MessageBus.instance().message(MessageType.RESIZED, None, ResizedData(self._letterbox, (self._height - 2 * self._margin, self._height * self._aspect_ratio - 2 * self._margin), (self._width, self._height)))
                    else:
                        self._letterbox = (self._margin, (self._height - (self._width * (1 / self._aspect_ratio))) / 2 + self._margin)
                        MessageBus.instance().message(MessageType.RESIZED, None, ResizedData(self._letterbox, (self._width * (1 / self._aspect_ratio) - 2 * self._margin, self._width - 2 * self._margin), (self._width, self._height)))
                elif event.type == pygame.MOUSEBUTTONUP:
                    MessageBus.instance().message(MessageType.MOUSECLICKED, self, MouseClickedData(pygame.mouse.get_pos()))
                elif event.type == pygame.MOUSEMOTION:
                    MessageBus.instance().message(MessageType.MOUSEMOVED, self, MouseMovedData(pygame.mouse.get_pos()))

            current_frame_ticks = pygame.time.get_ticks()
            delta_time = (current_frame_ticks - last_frame_ticks) / 1000.0
            last_frame_ticks = current_frame_ticks

            MessageBus.instance().message(MessageType.TICK, None, TickData(delta_time))

            buffer = RenderBuffer()
            MessageBus.instance().message(MessageType.RENDER, self, RenderData(buffer))

            self._screen.fill(pygame.Color(0, 0, 0))

            for renderables in buffer.buffer:
                for renderable in renderables:
                    if renderable[0] == RenderType.POLYGON:
                        pygame.gfxdraw.aapolygon(self._screen, renderable[1][1], renderable[1][0])
                        pygame.gfxdraw.filled_polygon(self._screen, renderable[1][1], renderable[1][0])
                    elif renderable[0] == RenderType.SURFACE:
                        self._screen.blit(renderable[1][1], renderable[1][0])

            pygame.display.update()

    def quit(self):
        self._quit = True
