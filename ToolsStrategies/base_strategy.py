from abc import ABC, abstractmethod
from SimElement.sim_base_class import SimBaseClass


class BaseStrategy(ABC):
    def __init__(self, element: SimBaseClass):
        self.element = element
        self.prev_x = 0
        self.prev_y = 0
        self.mouse_pressed = False

    def mouse_down(self, x: int, y: int):
        self.prev_x = x
        self.prev_y = y
        self.mouse_pressed = True

    def mouse_unpressed_move(self, x: int, y: int):
        return None

    def mouse_pressed_move(self, x: int, y: int):
        pass

    def mouse_double_click(self, x: int, y: int):
        pass

    def mouse_up(self, x: int, y: int):
        self.mouse_pressed = False
