import json
from pygame.sprite import Sprite
from pygame import Rect, Vector2
from pygame.surface import Surface
from exceptions import MethodNotImplemented
from renderer import Renderer
from action import Frame
from controls import Input, State

class GameObject(Sprite):
    def spawn(self) -> None:
        raise MethodNotImplemented("Implement `spawn` method")

    def is_alive(self) -> bool:
        raise MethodNotImplemented("Implement `is_alive` method")

    def collide(self, other: 'GameObject') -> bool:
        raise MethodNotImplemented("Implement `collide` method")

    def draw(self, renderer: Renderer) -> None:
        raise MethodNotImplemented("Implement `draw` method")

    def update(self, time: int) -> None:
        raise MethodNotImplemented("Implement `UPDATE` method")

class Ship(GameObject):
    SPRITE = 0

    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.__is_alive = True
        self.rect = Rect(0, 0, 13, 13)
        self.rect.center = (18, 220)
        self.frame = Frame(self.rect, Rect(3, 49, 13, 8), 6)
        self.input = None
        self.vel = Vector2(0, 0)
        self.speed = 2

    def set_input(self, input: Input) -> None:
        self.input = input

    def update(self, time: int) -> None:
        if self.input is None:
            return
        self.vel.x = self.input.get_direction().x * self.speed

        self.rect.left += self.vel.x
        self.frame.collision = self.rect

    def spawn(self) -> None:
        self.__is_alive = True

    def is_alive(self) -> bool:
        return self.__is_alive

    def collide(self, other: 'GameObject') -> bool:
        return self.rect.colliderect(other.rect)

    def draw(self, renderer: Renderer) -> None:
        renderer.draw(self.SPRITE, self.frame.src, self.frame.collision)

    def move_left(self):
        self.dir = self.LEFT
        self.vel.x = -1 * self.speed
        self.vel.y = 0

    def move_right(self):
        self.dir = self.RIGHT
        self.vel.x = self.speed
        self.vel.y = 0

    def move_up(self):
        self.dir = self.UP
        self.vel.y = self.speed
        self.vel.x = 0

    def move_down(self):
        self.dir = self.DOWN
        self.vel.y = -1 * self.speed
        self.vel.x = 0