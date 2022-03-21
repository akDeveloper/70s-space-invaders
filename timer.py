class Timer(object):
    def __init__(self, delay: int):
        self.delay: int = delay
        self.counter: int = 0

    def completed(self, time: int):
        self.counter += time
        if self.counter >= self.delay:
            return True
        return False

    def looped(self, time: int):
        self.counter += time
        if self.counter >= self.delay:
            self.counter = 0
            return True
        return False
