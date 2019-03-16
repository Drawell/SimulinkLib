from ToolsStrategies.base_strategy import BaseStrategy
from SimElement.sim_base_class import SimBaseClass
from SimElement.element_part_enum import ElementPartEnum as EPE
from Environment.environment import Environment

class ObserverTool(BaseStrategy):
    def __init__(self, element: Environment):
        super().__init__(element)

    def mouse_unpressed_move(self, x: int, y: int):
        element, part = self.element.get_element_by_coord(x, y)
        return part
