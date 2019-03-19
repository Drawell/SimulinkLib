from SimElement import ElementPartEnum as EPE
from SimElement.sim_box import SimBox
from SimElement.sim_socket import InputSocket, OutputSocket
from SimPainter.sim_painter import SimPainter


class SimConnection(SimBox):
    def __init__(self, env, x_start: int, y_start: int, x_end, y_end):
        super().__init__()
        self.env = env
        self.start_box = SimBox(x_start, y_start, 8, 8)
        self.end_box = SimBox(x_end, y_end, 8, 8)
        self.start_socket = None
        self.end_socket = None

    def get_start_box(self)->SimBox:
        return self.start_box

    def get_end_box(self)->SimBox:
        return self.end_box

    def get_start_socket(self)->OutputSocket:
        return self.start_socket

    def get_end_socket(self)->InputSocket:
        return self.end_socket

    def set_start_socket(self, socket: OutputSocket):
        self.start_socket = socket

    def set_end_socket(self, socket: InputSocket):
        self.end_socket = socket

    def paint(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        painter.set_pen_width(3)

        # start arrow
        if self.start_socket is not None:
            painter.set_pen_colour(0, 255, 0)
            self.start_box.x = self.start_socket.x
            self.start_box.y = self.start_socket.y
        else:
            painter.set_pen_colour(255, 0, 0)

        x1 = x_indent + self.start_box.x
        y1 = y_indent + self.start_box.y
        painter.draw_line(x1, y1 + 2, x1 + 6, y1 + 5)
        painter.draw_line(x1, y1 + 8, x1 + 6, y1 + 5)

        # end arrow
        if self.end_socket is not None:
            painter.set_pen_colour(0, 255, 0)
            self.end_box.x = self.end_socket.x
            self.end_box.y = self.end_socket.y
        else:
            painter.set_pen_colour(255, 0, 0)

        x2 = x_indent + self.end_box.x
        y2 = y_indent + self.end_box.y
        painter.draw_line(x2, y2 + 2, x2 + 6, y2 + 5)
        painter.draw_line(x2, y2 + 8, x2 + 6, y2 + 5)

        # line
        painter.set_pen_width(1)
        painter.set_pen_colour(0, 0, 0)
        painter.draw_line(x1 + 4, y1 + 4, x2 + 4, y2 + 4)

    def in_element(self, x: int, y: int) -> EPE:
        return EPE.NONED
        #return super().in_element(x, y)

