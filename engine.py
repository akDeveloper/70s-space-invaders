import pygame
from pygame.locals import QUIT, KEYUP, KEYDOWN, K_ESCAPE
from renderer import Renderer
from pygame.time import Clock
from pygame.event import get, Event
from controls import Controller, Input
from pygame import USEREVENT
from pygame.mouse import set_visible
from exceptions import MethodNotImplemented

class GameState(object):
    def __init__(self):
        pass

    def update(self, time: int, input: Input) -> None:
        raise MethodNotImplemented("Implement `update` method")

    def draw(self, renderer: Renderer) -> None:
        raise MethodNotImplemented("Implement `draw` method")

    def state(self) -> 'GameState':
        raise MethodNotImplemented("Implement `state` method")

    def on_event(self, e) -> None:
        raise MethodNotImplemented("Implement `on_event` method")


class Engine():
    FPS = 30  # 1/60th of second
    GAME_EVENT = USEREVENT + 1

    def __init__(self, renderer: Renderer):
        self.__renderer: Renderer = renderer
        self.__run = True
        self.controller = Controller()
        set_visible(False)

    def on_event(self, e: Event) -> None:
        if e.type == QUIT:
            self.on_exit()
        elif e.type == KEYUP:
            self.on_key_up(e)
        elif e.type == KEYDOWN:
            self.on_key_down(e)

    def __cleanup(self) -> None:
        pygame.quit()

    def on_exit(self) -> None:
        self.__run = False

    def on_key_down(self, e: Event):
        self.controller.key_down(e)

    def on_key_up(self, e: Event):
        if e.key == K_ESCAPE:
            self.__run = False
        self.controller.key_up(e)

    def run(self, state: GameState):
        clock: Clock = Clock()

        while(self.__run is True):
            for event in get():
                if event.type == self.GAME_EVENT:
                    state.on_event(event)
                    continue
                self.on_event(event)
            self.controller.on_event()
            state.update(clock.get_time(), self.controller)
            self.__renderer.cls()
            state.draw(self.__renderer)
            self.__renderer.draw_to_screen()
            state = state.state()
            clock.tick(self.FPS)
        self.__cleanup()
