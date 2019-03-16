from ToolsStrategies.base_strategy import BaseStrategy
from SimElement.sim_base_class import SimBaseClass


class MoveTool(BaseStrategy):
    def __init__(self, element: SimBaseClass, x: int = 0, y: int = 0):
        super().__init__(element)
        self.mouse_down(x, y)
        self.x_indent_in_box = (self.element.x - self.prev_x)
        self.y_indent_in_box = (self.element.y - self.prev_y)

    def mouse_pressed_move(self, x: int, y: int):
        self.element.move_to(x + self.x_indent_in_box, y + self.y_indent_in_box)
