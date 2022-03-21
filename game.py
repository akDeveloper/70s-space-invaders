from pygame.sprite import collide_rect
from engine import GameState
from controls import Input
from renderer import Renderer
from sprites import Ship

class LoadState(GameState):
    def __init__(self, renderer: Renderer) -> None:
        super().__init__()
        self.renderer = renderer

    def update(self, time: int, input: Input) -> None:
        pass

    def draw(self, renderer: Renderer) -> None:
        pass

    def state(self) -> GameState:
        return PlayState(self.renderer)

    def on_event(self, e) -> None:
        pass

class PlayState(GameState):
    def __init__(self, renderer: Renderer):
        renderer.register_image(Ship.SPRITE, "assets/sprites.png", (0, 0, 0), False)
        self.screen = renderer.screen()
        self.ship = Ship()

    def update(self, time: int, input: Input) -> None:
        self.ship.set_input(input)
        self.ship.update(time)

    def draw(self, renderer: Renderer) -> None:
        self.ship.draw(renderer)

    def state(self) -> 'GameState':
        return self



