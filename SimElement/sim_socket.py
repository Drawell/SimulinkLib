from abc import ABC, abstractmethod
from SimElement.sim_box import SimBox
from SimPainter import SimPainter


class Socket(SimBox, ABC):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 10)

    def __str__(self):
        return 'Not value' if self.get_value() is None else str(self.get_value())

    @abstractmethod
    def check(self) -> bool:
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


class InputSocket(Socket):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.input_socket = None

    def __str__(self):
        return 'Value = %s; %s' % ('nope' if self.get_value() is None else str(self.get_value()),
                                   'Bind' if self.input_socket else 'Not bind')

    def check(self)->bool:
        return self.input_socket is not None and self.input_socket.get_value() is not None

    def get_value(self):
        if self.input_socket is not None:
            return self.input_socket.get_value()

    def put_value(self, value):
        pass

    def bind_with(self, socket):
        if socket is not None and type(socket) is OutputSocket:
            self.input_socket = socket

    def unbind(self):
        self.input_socket = None

    def paint(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        painter.draw_line(self.x + x_indent, self.y + y_indent, self.x + x_indent + 10, self.y + y_indent + 5)
        painter.draw_line(self.x + x_indent, self.y + y_indent + 10, self.x + x_indent + 10, self.y + y_indent + 5)


class OutputSocket(Socket):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.value = None

    def __str__(self):
        return 'Not value' if self.get_value() is None else str(self.get_value())

    def check(self)->bool:
        return self.value is not None

    def get_value(self):
        return self.value

    def put_value(self, value):
        self.value = value

    def bind_with(self, socket):
        if type(socket) is InputSocket:
            socket.bind_with(self)

    def paint(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        painter.draw_line(self.x + x_indent, self.y + y_indent, self.x + x_indent + 10, self.y + y_indent + 5)
        painter.draw_line(self.x + x_indent, self.y + y_indent + 10, self.x + x_indent + 10, self.y + y_indent + 5)
