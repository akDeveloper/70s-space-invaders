from pygame.sprite import Sprite
from pygame import Rect, Vector2
from pygame.surface import Surface
from exceptions import MethodNotImplemented
from renderer import Renderer
from action import Frame
from controls import Input, State
from timer import Timer

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

class ShipBullet(GameObject):
    SPRITE = 0

    def __init__(self, boundary: Rect, position: tuple, *groups) -> None:
        super().__init__(*groups)
        self.__is_alive = True
        self.__explode = False
        self.rect = Rect(position[0], position[1], 1, 4)
        self.frame = Frame(self.rect, Rect(55, 53, 1, 4), 6)
        self.input = None
        self.speed = 6
        self.boundary = boundary
        self.timer = None

    def update(self, time: int) -> None:
        if self.__is_alive is False:
            return

        # When explotion time is passed, do not update sprite
        if self.timer != None and self.timer.completed(time):
            self.__is_alive = False
            self.__explode = False
            return

        if self.__explode is False:
            new_position = self.rect.top - self.speed
        else:
            new_position = self.rect.top #  When not in explode state, do not move sprite

        # When bullet reaches up boundary limit
        if new_position <= self.boundary.top and self.__explode is False:
            new_position = self.boundary.top
            self.rect = Rect(self.rect.left - 4, self.rect.top, 8, 8)
            self.frame = Frame(self.rect, Rect(58, 49, 8, 8), 6)
            self.__explode = True
            self.timer = Timer(180)

        self.rect.top = new_position
        self.frame.collision = self.rect

    def is_alive(self) -> bool:
        return self.__is_alive

    def draw(self, renderer: Renderer) -> None:
        renderer.draw(self.SPRITE, self.frame.src, self.frame.collision)

class Ship(GameObject):
    SPRITE = 0

    def __init__(self, boundary: Rect,  *groups) -> None:
        super().__init__(*groups)
        self.__is_alive = True
        self.rect = Rect(18, 220, 13, 8)
        self.frame = Frame(self.rect, Rect(3, 49, 13, 8), 6)
        self.input = None
        self.vel = Vector2(0, 0)
        self.speed = 2
        self.boundary = boundary
        self.bullets = []
        self.__score = 0

    def set_input(self, input: Input) -> None:
        self.input = input

    def score(self) -> int:
        return self.__score

    def update(self, time: int) -> None:
        if self.input is None:
            return

        if self.input.get_buttons().get_pressed() == State.B and len(self.bullets) == 0:
            self.fire()
        self.__update_bullets(time)

        self.vel.x = self.input.get_direction().x * self.speed

        new_position = self.rect.left + self.vel.x
        if new_position <= self.boundary.left \
            or new_position + self.rect.width >= self.boundary.right:
            return

        self.rect.left = new_position
        self.frame.collision = self.rect

    def fire(self) -> None:
        bullet = ShipBullet(self.boundary, (self.rect.left + 6, self.rect.top))
        self.bullets.append(bullet)

    def spawn(self) -> None:
        self.__is_alive = True

    def is_alive(self) -> bool:
        return self.__is_alive

    def collide(self, other: 'GameObject') -> bool:
        return self.rect.colliderect(other.rect)

    def draw(self, renderer: Renderer) -> None:
        renderer.draw(self.SPRITE, self.frame.src, self.frame.collision)
        for bullet in self.bullets:
            bullet.draw(renderer)

    def __update_bullets(self, time: int) -> None:
        for bullet in self.bullets:
            bullet.update(time)
            if bullet.is_alive() is False:
                self.bullets.remove(bullet)

class Letter(Sprite):
    SPRITE = 0

    def __init__(self, position: Rect, text: str, *groups) -> None:
        self.position = position
        self.text = text
        self.sources = {
            'A': Rect(1, 69, 8, 8),
            'B': Rect(11, 69, 8, 8),
            'C': Rect(21, 69, 8, 8),
            'D': Rect(31, 69, 8, 8),
            'E': Rect(41, 69, 8, 8),
            'F': Rect(51, 69, 8, 8),
            'G': Rect(61, 69, 8, 8),
            'H': Rect(71, 69, 8, 8),
            'I': Rect(1, 79, 8, 8),
            'J': Rect(11, 79, 8, 8),
            'K': Rect(21, 79, 8, 8),
            'L': Rect(31, 79, 8, 8),
            'M': Rect(41, 79, 8, 8),
            'N': Rect(51, 79, 8, 8),
            'O': Rect(61, 79, 8, 8),
            'P': Rect(71, 79, 8, 8),
            'Q': Rect(1, 89, 8, 8),
            'R': Rect(11, 89, 8, 8),
            'S': Rect(21, 89, 8, 8),
            'T': Rect(31, 89, 8, 8),
            'U': Rect(41, 89, 8, 8),
            'V': Rect(51, 89, 8, 8),
            'W': Rect(61, 89, 8, 8),
            'X': Rect(71, 89, 8, 8),
            'Y': Rect(1, 99, 8, 8),
            'Z': Rect(11, 99, 8, 8),
            '0': Rect(21, 99, 8, 8),
            '1': Rect(31, 99, 8, 8),
            '2': Rect(41, 99, 8, 8),
            '3': Rect(51, 99, 8, 8),
            '4': Rect(61, 99, 8, 8),
            '5': Rect(71, 99, 8, 8),
            '6': Rect(1, 109, 8, 8),
            '7': Rect(11, 109, 8, 8),
            '8': Rect(21, 109, 8, 8),
            '9': Rect(31, 109, 8, 8),
            '<': Rect(41, 109, 8, 8),
            '>': Rect(51, 109, 8, 8),
            '=': Rect(61, 109, 8, 8),
            '*': Rect(71, 109, 8, 8),
            '?': Rect(1, 119, 8, 8),
            '-': Rect(11, 119, 8, 8),
        };

    def update(self, time: int):
        pass

    def set_text(self, text: str):
        self.text = text

    def draw(self, renderer: Renderer) -> None:
        word = str(self.text)
        word = word.zfill(5)
        chars = [char for char in word]
        for index, char in enumerate(chars):
            letter_on_sheet = self.sources.get(char)
            where_to_put = Rect(self.position.left + (index * 8), self.position.top, 8, 8)
            renderer.draw(self.SPRITE, letter_on_sheet, where_to_put)
