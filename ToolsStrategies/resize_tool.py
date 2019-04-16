from ToolsStrategies import BaseState
from PySimCore import SimBox, ElementPartEnum as EPE


class ResizeTool(BaseState):
    def __init__(self, element: SimBox, part: EPE, x: int = 0, y: int = 0):
        super().__init__(element)
        self.mouse_down(x, y)
        self.part = part

    def mouse_pressed_move(self, x: int, y: int):

        #if self.part == EPE.CENTER:
        #    pass

        dx, dy = (x - self.prev_x), (y - self.prev_y)
        self.mouse_down(x, y)

        if self.part == EPE.NONE:
            self.element.resize(self.element.width + dx, self.element.height + dy)
            return

        if self.part in [EPE.RIGHT, EPE.LEFT]:  # forbid to resize horizontally
            dy = 0
        if self.part in [EPE.TOP, EPE.BOTTOM]:  # forbid to resize vertically
            dx = 0

        if self.part in [EPE.LEFT, EPE.BOTTOM_LEFT, EPE.TOP_LEFT]:
            self.element.move_to(self.element.x + dx, self.element.y)
            dx = -dx

        if self.part in [EPE.TOP, EPE.TOP_LEFT, EPE.TOP_RIGHT]:
            self.element.move_to(self.element.x, self.element.y + dy)
            dy = -dy

        self.element.resize(self.element.width + dx, self.element.height + dy)
