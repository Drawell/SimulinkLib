from ToolsStrategies import BaseStrategy
from PySimCore import SimCompositeElement


class ObserverTool(BaseStrategy):
    def __init__(self, element: SimCompositeElement):
        super().__init__(element)

    def mouse_unpressed_move(self, x: int, y: int):
        element, part = self.element.find_anything_by_coord(x, y)
        #print(element, part)
        return part
