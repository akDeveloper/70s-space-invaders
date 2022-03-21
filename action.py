from pygame import Rect


class Frame(object):
    def __init__(self, col: Rect, src: Rect, delay: int):
        """
        Parameters
        ----------
        col : Rect
            The actual position of frame in the level.
        src : Rect
            The source rectangle of tile image.
        delay : int
            The time to display the current frame.
        """
        self.collision: Rect = col
        self.src: Rect = src
        self.delay = delay


class Action(object):
    def __init__(self, frames: list):
        self.tick: int = 0
        self.index: int = 0
        self.frames: list = frames

    def next_frame(self) -> Frame:
        frame: Frame = self.frames[self.index]
        if self.tick > frame.delay:
            self.tick = 0
            self.index += 1
            if self.index >= len(self.frames):
                self.index = len(self.frames) - 1
        self.tick += 1
        return frame

    def reset(self) -> None:
        self.tick = 0
        self.index = 0

    def is_completed(self) -> bool:
        return self.index == (len(self.frames) - 1)
