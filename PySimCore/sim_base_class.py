from abc import ABC, abstractmethod
from PySimCore import SimBox, ElementPartEnum as EPE, RotationPositionEnum as RPE, CheckExceptionEnum as CHE, \
    InputSocket, SimPainter, OutputSocket, sim_property
import xml.etree.ElementTree as xml

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
        self.__set_of_indexes__ = []
        self.font = 9
        self.radius_for_resize = 3

        self.update(kwargs)

    def __str__(self):
        p = '{ '
        for key, value in self.properties.items():
            p += key + ': ' + str(value) + ', '
        return 'Element ' + self.name + p + '}'

    def update(self, new_properties: dict):
        pass

    @sim_property
    def name(self):
        pass

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        pass

    def resize(self, w: int, h: int):
        super().resize(w, h)
        self.move_sockets(self.x, self.y)
        self.set_sockets_to_positions()

    def move_to(self, x: int, y: int):
        super().move_to(x, y)
        self.move_sockets(x, y)
        self.set_sockets_to_positions()

    def check(self, context: dict) -> dict:
        check_result = {}

        # all variables must to be inited
        for var in self.get_local_variables():
            if var not in context:
                if CHE.VARIABLE_REQUIRED not in check_result.keys():
                    check_result[CHE.VARIABLE_REQUIRED] = []
                check_result[CHE.VARIABLE_REQUIRED].append(var)

        # check for inputs
        for socket in self.__input_sockets__:
            if socket.check() == CHE.DISCONNECTED_SOCKET:
                if CHE.DISCONNECTED_SOCKET not in check_result.keys():
                    check_result[CHE.DISCONNECTED_SOCKET] = []
                check_result[CHE.DISCONNECTED_SOCKET].append(
                    'disconnected socket in name: %s with index %s' % (socket.name, socket.index))
            elif socket.check() == CHE.UNCHECKED_SOCKET:
                if CHE.UNCHECKED_SOCKET not in check_result.keys():
                    check_result[CHE.UNCHECKED_SOCKET] = []
                check_result[CHE.UNCHECKED_SOCKET].append('Socket unchecked: %s' % socket.index)

        if len(check_result) == 0:
            for socket in self.__output_sockets__:
                socket.set_checked()

        return check_result

    def set_sockets_unchecked(self):
        for socket in self.__output_sockets__:
            socket.set_checked(False)
        for socket in self.__input_sockets__:
            socket.set_checked(False)

    @abstractmethod
    def init_simulation(self, context: dict):
        pass

    @abstractmethod
    def iterate(self, time: float, context: dict):
        pass

    def get_local_variables(self) -> list:
        return []

    def show(self):
        return False

    @staticmethod
    @abstractmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        pass

    # def paint(self, painter: SimPainter, x: float = 0, y: float = 0, scale: float = 1):
    # pass

    def in_element(self, x: int, y: int) -> EPE:
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

    def new_input_socket(self, position: RPE = RPE.RIGHT):
        if len(self.__set_of_indexes__) == 0:
            idx = self.output_sockets_count() + self.input_sockets_count()
        else:
            self.__set_of_indexes__.sort(reverse=True)
            idx = self.__set_of_indexes__.pop()

        socket = InputSocket(idx, self.name, self.x, self.y, position)
        self.__input_sockets__.append(socket)
        SimBaseClass.set_sockets_to_positions(self)
        return socket

    def new_output_socket(self, position: RPE = RPE.RIGHT):
        if len(self.__set_of_indexes__) == 0:
            idx = self.output_sockets_count() + self.input_sockets_count()
        else:
            self.__set_of_indexes__.sort(reverse=True)
            idx = self.__set_of_indexes__.pop()

        socket = OutputSocket(idx, self.name, self.x, self.y, position)
        self.__output_sockets__.append(socket)
        SimBaseClass.set_sockets_to_positions(self)
        return socket

    def delete_all_input_sockets(self):
        for socket in self.__input_sockets__:
            socket.unbind()
            self.__set_of_indexes__.append(socket.index)
            self.__input_sockets__.remove(socket)
            # del socket

        self.set_sockets_to_positions()

    def delete_all_output_sockets(self):
        for socket in self.__output_sockets__:
            socket.unbind()
            self.__set_of_indexes__.append(socket.index)
            self.__output_sockets__.remove(socket)
        self.set_sockets_to_positions()

    def delete_socket(self, socket):
        socket.unbind()
        if socket in self.__output_sockets__:
            self.__set_of_indexes__.append(socket.index)
            self.__output_sockets__.remove(socket)

        elif socket in self.__input_sockets__:
            self.__set_of_indexes__.append(socket.index)
            self.__input_sockets__.remove(socket)

        del socket
        self.set_sockets_to_positions()

    def get_input_socket(self, index: int) -> InputSocket:
        for socket in self.__input_sockets__:
            if socket.index == index:
                return socket
        return None

    def get_output_socket(self, index: int) -> OutputSocket:
        for socket in self.__output_sockets__:
            if socket.index == index:
                return socket
        return None

    def move_sockets(self, x: int, y: int):
        for i, s in enumerate(self.__input_sockets__):
            s.move_to(x, y)

        for i, s in enumerate(self.__output_sockets__):
            s.move_to(x, y)

    def set_sockets_to_positions(self):
        step = self.height / (self.input_sockets_count() + 1)
        y = step
        for i, s in enumerate(self.__input_sockets__):
            s.set_to_pos(-10, y - 5)
            y += step

        step = self.height / (self.output_sockets_count() + 1)
        y = step
        for i, s in enumerate(self.__output_sockets__):
            s.set_to_pos(self.width, y - 5)
            y += step
