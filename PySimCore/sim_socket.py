from abc import ABC, abstractmethod
from PySimCore import SimBox, SimPainter, SocketPositionEnum as SPE, CheckExceptionEnum as CHE

point1_multiplier = {SPE.TOP: [1/2, 1],
          SPE.BOTTOM: [1/2, 0],
          SPE.RIGHT: [0, 1/2],
          SPE.LEFT: [1, 1/2]}

point2_multiplier = {SPE.TOP: [0, 0],
          SPE.BOTTOM: [1, 1],
          SPE.RIGHT: [1, 0],
          SPE.LEFT: [0, 1]}

point3_multiplier = {SPE.TOP: [1, 0],
          SPE.BOTTOM: [0, 1],
          SPE.RIGHT: [1, 1],
          SPE.LEFT: [0, 0]}


class Socket(SimBox, ABC):
    def __init__(self, index: int, name: str, x: int, y: int, position: SPE):
        self.size = 10
        super().__init__(x, y, self.size, self.size)
        self.position = position
        self.index = index
        self.name = name
        self.x_in_parent = 0
        self.y_in_parent = 0
        self.checked = False

    def __str__(self):
        return 'Socket: ' + 'Not value' if self.get_value() is None else str(self.get_value())

    def resize(self, w: int, h: int):
        pass

    def move_to(self, x: int, y: int):
        super().move_to(x, y)
        self.x_in_parent = 0
        self.y_in_parent = 0

    def set_to_pos(self, x: int, y: int):
        self.move_to(self.x - self.x_in_parent + x, self.y - self.y_in_parent + y)
        self.x_in_parent = x
        self.y_in_parent = y

    def set_checked(self, is_checked=True):
        self.checked = is_checked

    @abstractmethod
    def check(self) -> CHE:
        pass

    @abstractmethod
    def get_value(self):
        pass

    @abstractmethod
    def put_value(self, value):
        pass

    @abstractmethod
    def bind_with(self, socket):
        pass

    @abstractmethod
    def unbind(self):
        pass

    def paint(self, painter: SimPainter, x: float = 0, y: float = 0, scale: float = 1):
        x1 = x + self.x + self.size * point1_multiplier[self.position][0]
        y1 = y + self.y + self.size * point1_multiplier[self.position][1]
        x2 = x + self.x + self.size * point2_multiplier[self.position][0]
        y2 = y + self.y + self.size * point2_multiplier[self.position][1]
        x3 = x + self.x + self.size * point3_multiplier[self.position][0]
        y3 = y + self.y + self.size * point3_multiplier[self.position][1]

        painter.draw_line(x1, y1, x3, y3)
        painter.draw_line(x1, y1, x2, y2)


class InputSocket(Socket):
    def __init__(self, index: int, name: str, x=0, y=0, position: SPE = SPE.LEFT):
        super().__init__(index, name, x, y, position)
        self.output_socket = None

    def __str__(self):
        return 'Input Socket: Value = %s; %s' % ('nope' if self.get_value() is None else str(self.get_value()),
                                   'Bind' if self.output_socket else 'Not bind')

    def check(self) -> CHE:
        if self.output_socket is None:
            return CHE.DISCONNECTED_SOCKET
        elif self.output_socket.check() != CHE.OK:
            return CHE.UNCHECKED_SOCKET
        return CHE.OK

    def get_value(self):
        if self.output_socket is not None:
            return self.output_socket.get_value()

    def put_value(self, value):
        pass

    def is_bind(self):
        return self.output_socket is not None

    def bind_with(self, socket):
        if socket is not None and type(socket) is OutputSocket:
            self.output_socket = socket

    def unbind(self):
        self.output_socket = None


class OutputSocket(Socket):
    def __init__(self, index: int, name: str, x=0, y=0, position: SPE = SPE.LEFT):
        super().__init__(index, name, x, y, position)
        self.value = None

    def __str__(self):
        return 'Output Socket: Not value' if self.get_value() is None else str(self.get_value())

    def check(self) -> CHE:
        if self.checked:
            return CHE.OK

        return CHE.UNCHECKED_SOCKET

    def get_value(self):
        return self.value

    def put_value(self, value):
        self.value = value

    def bind_with(self, socket):
        if type(socket) is InputSocket:
            socket.bind_with(self)

    def unbind(self):
        pass
