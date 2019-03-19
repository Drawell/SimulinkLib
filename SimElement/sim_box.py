from SimElement import ElementPartEnum as EPE
from SimPainter import SimPainter


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

    def paint(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        pass
        #painter.draw_rectangle(x_indent, y_indent, 10, 10)

    def in_element(self, x: int, y: int) -> EPE:
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            return EPE.CENTER

        return EPE.NONE
