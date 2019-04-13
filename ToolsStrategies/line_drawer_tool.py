from ToolsStrategies import BaseStrategy
from PySimCore import SimConnection
from PySimCore import SimBox
from Environment import Environment


class LineDrawerTool(BaseStrategy):
    def __init__(self, x: int, y: int, connection: SimConnection, box: SimBox, env: Environment):
        super().__init__(connection)
        self.mouse_down(x, y)
        self.box = box
        self.env = env
        self.x_indent_in_box = (self.element.x - self.prev_x)
        self.y_indent_in_box = (self.element.y - self.prev_y)

    def mouse_pressed_move(self, x: int, y: int):
        #self.box.move_to(x + self.x_indent_in_box, y + self.y_indent_in_box)
        self.box.move_to(x - self.env.cmp.x, y - self.env.cmp.y)

        self.env.change_connection(self.element)

    def mouse_up(self, x: int, y: int):
        super().mouse_up(x, y)
        #self.env.try_to_connect(self.element)

