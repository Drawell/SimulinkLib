from ToolsStrategies.base_strategy import BaseStrategy
from SimElement.sim_connection import SimConnection
from SimElement.sim_box import SimBox
from Environment.environment import Environment


class LineDrawerTool(BaseStrategy):
    def __init__(self, x: int, y: int, connection: SimConnection, box: SimBox, env: Environment):
        super().__init__(connection)
        self.mouse_down(x, y)
        self.box = box
        self.env = env

    def mouse_pressed_move(self, x: int, y: int):
        self.box.move_to(x, y)
        self.env.try_to_connect(self.element)

    def mouse_up(self, x: int, y: int):
        super().mouse_up(x, y)
        self.env.try_to_connect(self.element)

