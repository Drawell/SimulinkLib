from ToolsStrategies import BaseStrategy
from Environment import Environment


class ObserverTool(BaseStrategy):
    def __init__(self, element: Environment):
        super().__init__(element)

    def mouse_unpressed_move(self, x: int, y: int):
        element, part = self.element.get_element_by_coord(x, y)
        return part
