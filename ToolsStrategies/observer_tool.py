from ToolsStrategies import BaseState
from PySimCore import SimCompositeElement


class ObserverTool(BaseState):
    def __init__(self, element: SimCompositeElement):
        super().__init__(element)

    def mouse_unpressed_move(self, x: int, y: int):
        element, part = self.element.find_anything_by_coord(x, y)
        #print(element, part)
        return part

    def mouse_double_click(self, x: int, y: int):
        element, part = self.element.find_anything_by_coord(x, y)
        return element, part