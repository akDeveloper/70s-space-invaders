from pygame.sprite import collide_rect
from pygame import Rect, Vector2
from engine import GameState
from controls import Input
from renderer import Renderer
from sprites import Ship, Letter, AlienGroup

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
        self.boundary = Rect(9, 38, 205, 205)
        self.ship = Ship(self.boundary)
        self.alien = AlienGroup(self.boundary, '1', Vector2(34, 68))
        self.player_one_score_label = Letter(Rect(8, 12, 64, 8), 'SCORE<1>')
        self.player_two_score_label = Letter(Rect(152, 12, 64, 8), 'SCORE<2>')
        self.player_one_score = Letter(Rect(24, 28, 40, 8), '')
        self.hi_score = Letter(Rect(88, 28, 40, 8), '')
        self.hi_score_label = Letter(Rect(80, 12, 64, 8), 'HI-SCORE')

    def update(self, time: int, input: Input) -> None:
        self.ship.set_input(input)
        self.ship.update(time)
        self.alien.update(time)
        self.player_one_score.set_text(self.ship.score())

    def draw(self, renderer: Renderer) -> None:
        self.ship.draw(renderer)
        self.alien.draw(renderer)
        self.player_one_score.draw(renderer)
        self.player_one_score_label.draw(renderer)
        self.player_two_score_label.draw(renderer)
        self.hi_score.draw(renderer)
        self.hi_score_label.draw(renderer)

    def state(self) -> 'GameState':
        return self



