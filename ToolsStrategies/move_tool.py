from ToolsStrategies import BaseStrategy
from PySimCore import SimBox


class MoveTool(BaseStrategy):
    def __init__(self, element: SimBox, x: int = 0, y: int = 0):
        super().__init__(element)
        self.mouse_down(x, y)
        self.x_indent_in_box = (self.element.x - self.prev_x)
        self.y_indent_in_box = (self.element.y - self.prev_y)

    def mouse_pressed_move(self, x: int, y: int):
        xx = self.element.x
        yy = self.element.y
        self.element.move_to(x + self.x_indent_in_box, y + self.y_indent_in_box)
