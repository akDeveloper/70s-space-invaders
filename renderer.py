from pickle import TRUE
from pygame import Surface, Rect, image, init, HWSURFACE, DOUBLEBUF, FULLSCREEN
from pygame.transform import scale
from pygame.display import set_mode, update
from exceptions import MethodNotImplemented

class Renderer(object):
    def __init__(self, bb_width: int, bb_height: int, sc_width: int, sc_height: int, fullscreen: bool = False):
        pass

    def draw_to_screen(self) -> None:
        raise MethodNotImplemented("Implement `draw_to_screen` method")

    def cls(self) -> None:
        raise MethodNotImplemented("Implement `cls` method")

    def register_image(self, name: int, filepath: str) -> None:
        raise MethodNotImplemented("Implement `register_image` method")

    def draw(self, name: int, src: Rect, dest: Rect) -> None:
        raise MethodNotImplemented("Implement `draw` method")

    def draw_with_image(self, image: Surface, dest: Rect, src: Rect, flags: int = 0) -> None:
        raise MethodNotImplemented("Implement `draw` method")

    def draw_to_other(self, other: Surface, spr: int, src: Rect, dest: Rect, flags: int = 0) -> None:
        raise MethodNotImplemented("Implement `draw_to_other` method")

    def screen(self) -> tuple:
        raise MethodNotImplemented("Implement `screen` method")


class SdlRenderer(Renderer):
    def __init__(self, bb_width: int, bb_height: int, sc_width: int, sc_height: int, fullscreen: bool = False):
        init() # Initialize pygame
        self.bb_size = (bb_width, bb_height)
        self.__images: list = []
        self.__size = (sc_width, sc_height)
        if fullscreen is True:
            self.__screen = set_mode(self.__size, HWSURFACE | DOUBLEBUF | FULLSCREEN)
        else:
            self.__screen = set_mode(self.__size)
        """ backbuffer Surface for handling the small graphics """
        self.__backbuffer = Surface(self.bb_size)

    def draw_to_screen(self) -> None:
        self.__backbuffer.convert_alpha()
        """ upscale backbuffer to screen """
        scale(self.__backbuffer, self.__size, self.__screen)
        update()

    def cls(self) -> None:
        self.__backbuffer.fill((21, 21, 21))

    def register_image(self, spr: int, filepath: str, color: tuple, transparent: bool) -> None:
        surface = image.load(filepath)
        if transparent is True:
            surface.convert_alpha()
        else:
            surface.set_colorkey(color)
        self.__images.insert(spr, surface)

    def draw(self, spr: int, src: Rect, dest: Rect, flags: int = 0) -> None:
        self.__backbuffer.blit(self.__images[spr], dest, src, flags)

    def draw_with_image(self, image: Surface, dest: Rect, src: Rect, flags: int = 0) -> None:
        self.__backbuffer.blit(image, dest, src, flags)

    def draw_to_other(self, other: Surface, spr: int, src: Rect, dest: Rect, flags: int = 0) -> None:
        other.blit(self.__images[spr], dest, src, flags)

    def screen(self) -> tuple:
        return self.bb_size
