from abc import ABC, abstractmethod
from SimElement.sim_socket import InputSocket, OutputSocket
from SimElement.element_part_enum import ElementPartEnum as EPE
from SimElement.sim_box import SimBox
from SimPainter import SimPainter

part_map = [[EPE.TOP_LEFT, EPE.TOP, EPE.TOP_RIGHT],
            [EPE.LEFT, EPE.CENTER, EPE.RIGHT],
            [EPE.BOTTOM_LEFT, EPE.BOTTOM, EPE.BOTTOM_RIGHT]]


class SimBaseClass(SimBox, ABC):
    def __init__(self, x: int, y: int, kwargs):
        width = kwargs['width'] if 'width' in kwargs else 50
        height = kwargs['height'] if 'height' in kwargs else 50
        super().__init__(x, y, width, height)
        self.name = kwargs['name'] if 'name' in kwargs else self.get_name()
        self.__input_sockets__ = []
        self.__output_sockets__ = []
        self.font = 10
        self.radius_for_resize = 3

    def resize(self, w: int, h: int):
        super().resize(max(w, 32), max(h, 32))
        self.__set_sockets_to_positions__()

    def move_to(self, x: int, y: int):
        super().move_to(x, y)
        self.__set_sockets_to_positions__()

    @abstractmethod
    def make_step(self, time: float):
        pass

    @staticmethod
    def get_name()->str:
        pass

    @staticmethod
    @abstractmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        pass

    def paint(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        pass

    def in_element(self, x: int, y: int)-> EPE:
        radius = self.radius_for_resize
        if self.x + self.width < x or x < self.x \
                or self.y + self.height < y or y < self.y:
            return EPE.NONE

        top = abs(y - self.y) < radius
        bottom = abs(y - self.y - self.height) < radius
        right = abs(x - self.x - self.width) < radius
        left = abs(x - self.x) < radius

        x = 0 if top else 2 if bottom else 1
        y = 0 if left else 2 if right else 1

        return part_map[x][y]

    def input_sockets_iter(self):
        return self.__input_sockets__.__iter__()

    def output_sockets_iter(self):
        return self.__output_sockets__.__iter__()

    def input_sockets_count(self):
        return len(self.__input_sockets__)

    def output_sockets_count(self):
        return len(self.__output_sockets__)

    def new_input_socket(self):
        socket = InputSocket()
        self.__input_sockets__.append(socket)
        self.__set_sockets_to_positions__()
        return socket

    def new_output_socket(self):
        socket = OutputSocket()
        self.__output_sockets__.append(socket)
        self.__set_sockets_to_positions__()
        return socket

    def __set_sockets_to_positions__(self):
        step = self.height / (self.input_sockets_count() + 1)
        y = step
        for i, s in enumerate(self.__input_sockets__):
            s.move_to(self.x - 10, self.y + y - 5)
            y += step

        step = self.height / (self.output_sockets_count() + 1)
        y = step
        for i, s in enumerate(self.__output_sockets__):
            s.move_to(self.x + self.width, self.y + y - 5)
            y += step


def paint_func(func):
    def wrapped(self: SimBaseClass, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        painter.set_pen_width(3)

        for s in self.input_sockets_iter():
            s.paint(painter, x_indent, y_indent, scale)

        for s in self.output_sockets_iter():
            s.paint(painter, x_indent, y_indent, scale)

        painter.set_pen_width(1)
        func(self, painter, x_indent, y_indent, scale)

    return wrapped
