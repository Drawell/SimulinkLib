

class SimBox:
    def __init__(self, x: int = 0, y: int = 0, w: int = 0, h: int = 0):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.dirty = True

    def move_to(self, x: int, y: int):
        self.x = x
        self.y = y
        self.dirty = True

    def resize(self, w: int, h: int):
        self.width = w
        self.height = h
        self.dirty = True
