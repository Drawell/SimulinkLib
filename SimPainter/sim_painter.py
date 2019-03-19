from abc import ABC, abstractmethod


class SimPainter(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def set_pen_width(self, width):
        pass

    @abstractmethod
    def set_pen_colour(self, r:int, g:int, b:int):
        pass

    @abstractmethod
    def draw_rectangle(self, x: float, y: float, w: float, h: float):
        pass

    @abstractmethod
    def draw_line(self, x1: float, y1: float, x2: float, y2: float):
        pass

    @abstractmethod
    def draw_text(self, x: float, y: float, text: str, font_size: int):
        pass

    @abstractmethod
    def draw_curve(self, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float):
        pass

    @abstractmethod
    def clear(self):
        pass
