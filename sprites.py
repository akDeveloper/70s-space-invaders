from re import L
from pygame.sprite import Sprite
from pygame import Rect, Vector2
from pygame.surface import Surface
from exceptions import MethodNotImplemented
from renderer import Renderer
from action import Frame, Action
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
        raise MethodNotImplemented("Implement `update` method")

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
        for bullet in self.bullets:
            if bullet.rect.colliderect(other.rect):
                self.bullets.remove(bullet)
                self.__score += other.points()
                return True

    def draw(self, renderer: Renderer) -> None:
        renderer.draw(self.SPRITE, self.frame.src, self.frame.collision)
        for bullet in self.bullets:
            bullet.draw(renderer)

    def __update_bullets(self, time: int) -> None:
        for bullet in self.bullets:
            bullet.update(time)
            if bullet.is_alive() is False:
                self.bullets.remove(bullet)

class Alien(GameObject):
    SPRITE = 0

    def __init__(self, boundary: Rect, type: str, pos: Vector2, *groups) -> None:
        self.boundary = boundary
        self.speed = 2
        self.dive = 8
        self.__is_alive = True
        self.type = type
        self.action = self.__create_action(type, pos)
        self.frame = self.action.next_frame()
        self.dir = 1
        self.rect = Rect(pos.x, pos.y, self.frame.collision.w, self.frame.collision.h)
        self.walk_timer = 0
        self.speed_delay = 1000
        self.changed = False
        self.frame_index = 0
        self.__explode = False
        self.__explode_timer = 0

    def update(self, time: int) -> None:
        self.walk_timer += time
        if self.__is_alive is False:
            return

        if self.__explode_timer >= 90:
            self.__is_alive = False
            self.__explode = False
            self.__explode_timer = 0
            return

        if self.__explode is True:
            self.__explode_timer += time
            self.frame_index = 2
            self.frame = self.action.frames[self.frame_index]
            self.frame.collision.topleft = self.rect.topleft

        if not self.walk_timer > self.speed_delay:
            return

        self.walk_timer = 0
        if self.__explode is False:
            self.frame_index = 1 if self.frame_index == 0 else 0
            self.frame = self.action.frames[self.frame_index]

        vel = Vector2(0, 0)
        vel.x += self.speed * self.dir

        self.changed = False

        if self.rect.left + vel.x <= self.boundary.left \
            or self.rect.right + vel.x >= self.boundary.right:
            self.changed = True

        self.rect.left += vel.x
        self.rect.top += vel.y

        for frame in self.action.frames:
            frame.collision.topleft = self.rect.topleft

    def fire(self) -> None:
        pass

    def toggle(self) -> None:
        self.dir = self.dir * -1
        self.rect.top += self.dive
        self.changed = False
        self.frame.collision.topleft = self.rect.topleft

    def spawn(self) -> None:
        self.__is_alive = True

    def is_alive(self) -> bool:
        return self.__is_alive

    def is_exploding(self) -> bool:
        return self.__explode

    def explode(self) -> None:
        self.__explode = True

    def collide(self, other: 'GameObject') -> bool:
        """  Never used """
        return self.rect.colliderect(other.rect)

    def draw(self, renderer: Renderer) -> None:
        renderer.draw(self.SPRITE, self.frame.src, self.frame.collision)

    def points(self) -> int:
        if self.type == '1':
            return 30
        elif self.type == '2':
            return 20
        elif self.type == '3':
            return 10
        return 0


    def __create_action(self, type: str, pos: Vector2) -> Action:
        if type == '1':
            return Action([
                Frame(Rect(pos.x, pos.y, 8, 8), Rect(5, 1, 8, 8), 1),
                Frame(Rect(pos.x, pos.y, 8, 8), Rect(5, 11, 8, 8), 1),
                Frame(Rect(pos.x, pos.y, 8, 8), Rect(56, 1, 13, 8), 1)
            ])
        elif type == '2':
            return Action([
                Frame(Rect(pos.x, pos.y, 11, 8), Rect(22, 1, 11, 8), 1),
                Frame(Rect(pos.x, pos.y, 11, 8), Rect(22, 11, 11, 8), 1),
                Frame(Rect(pos.x, pos.y, 11, 8), Rect(56, 1, 13, 8), 1)
            ])
        elif type == '3':
            return Action([
                Frame(Rect(pos.x, pos.y, 12, 8), Rect(39, 1, 12, 8), 1),
                Frame(Rect(pos.x, pos.y, 12, 8), Rect(39, 11, 12, 8), 1),
                Frame(Rect(pos.x, pos.y, 12, 8), Rect(56, 1, 13, 8), 1)
            ])

class AlienGroup(GameObject):
    def __init__(self, boundary: Rect, type: str, pos: Vector2, *groups) -> None:
        self.aliens = []
        self.changed = False
        self.__to_remove = []
        for i in range(0, 11):
            new_pos = Vector2(pos.x + (16 * i), pos.y)
            self.aliens.append(Alien(boundary, type, new_pos))

    def update(self, time: int) -> None:
        self.changed = False

        for alien in self.aliens:
            alien.update(time)

        for alien in self.__to_remove:
            if alien.is_alive() is False:
                self.__to_remove.remove(alien)
                self.aliens.remove(alien)

        self.__has_reached_boundaries()

    def __has_reached_boundaries(self) -> bool:
        for alien in self.aliens:
            if alien.changed is True:
                self.changed = True
                return

    def toggle(self):
        for alien in self.aliens:
            alien.toggle()

    def spawn(self) -> None:
        self.__is_alive = True

    def is_alive(self) -> bool:
        return self.__is_alive

    def collide(self, other: 'GameObject') -> bool:
        for alien in self.aliens:
            if alien.is_exploding() is False and other.collide(alien):
                alien.explode()
                self.__to_remove.append(alien)
                return True

    def draw(self, renderer: Renderer) -> None:
        for alien in self.aliens:
            alien.draw(renderer)

    def count(self) -> int:
        return len(self.aliens)

    def update_speed(self, delay: int) -> None:
        for alien in self.aliens:
            alien.speed_delay = delay


class AllAliens(GameObject):
    def __init__(self, boundary: Rect, *groups) -> None:
        self.groups = []
        self.groups.append(AlienGroup(boundary, '1', Vector2(34, 68)))
        self.groups.append(AlienGroup(boundary, '2', Vector2(33, 83)))
        self.groups.append(AlienGroup(boundary, '2', Vector2(33, 98)))
        self.groups.append(AlienGroup(boundary, '3', Vector2(32, 113)))
        self.groups.append(AlienGroup(boundary, '3', Vector2(32, 128)))

    def update(self, time: int) -> None:
        for group in self.groups:
            group.update(time)

        reached_boundaries = self.__has_reached_boundaries()
        if reached_boundaries:
            for group in self.groups:
                group.toggle()

        count = self.count()

        if count < 45:
            self.update_speed(700)
        elif count < 35:
            self.update_speed(200)
        elif count < 25:
            self.update_speed(100)
        elif count < 15:
            self.update_speed(50)
        elif count < 5:
            self.update_speed(10)

    def __has_reached_boundaries(self) -> bool:
        for group in self.groups:
            if group.changed is True:
                return True

    def spawn(self) -> None:
        self.__is_alive = True

    def is_alive(self) -> bool:
        return self.__is_alive

    def collide(self, other: 'GameObject') -> bool:
        for group in self.groups:
            if group.collide(other):
                return True

    def draw(self, renderer: Renderer) -> None:
        for group in self.groups:
            group.draw(renderer)

    def update_speed(self, delay: int) -> None:
        for group in self.groups:
            group.update_speed(delay)

    def count(self) -> int:
        count = 0
        for group in self.groups:
            count += group.count()
        return count

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
