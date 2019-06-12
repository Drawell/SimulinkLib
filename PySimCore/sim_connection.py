from PySimCore import ElementPartEnum as EPE, SimBox, InputSocket, OutputSocket, SimPainter
#from PySimCore.sim_composite_element import SimCompositeElement
import xml.etree.ElementTree as xml


# In this class x, y = start_box.x, start_box.y and width, height = end_box.x, end_box.y

class SimConnection(SimBox):
    def __init__(self, cmp, x_start: int, y_start: int, x_end: int, y_end: int):
        super().__init__(x_start, y_start, x_end, y_end)
        self.cmp = cmp
        self.start_box = SimBox(x_start, y_start, 8, 8)
        self.end_box = SimBox(x_end, y_end, 8, 8)
        #self.radius = 5
        self.output_socket = None
        self.input_socket = None

    def __str__(self):
        i_s = 'input ' + 'NOT' if self.input_socket is None else 'CONNECTED'
        o_s = 'output ' + 'NOT' if self.output_socket is None else 'CONNECTED'
        return 'Connection: ' + i_s + '; ' + o_s

    def move_to(self, x: int, y: int):  # moving start
        super().move_to(x, y)
        self.start_box.move_to(x, y)

        #self.output_socket = None

        # try to connect
        # can connect to output
        socket = self.cmp.find_output_socket_by_coord([
            (self.x,                        self.y),
            (self.x + self.start_box.width, self.y + y),
            (self.x,                        self.y + self.start_box.height),
            (self.x + self.start_box.width, self.y + self.start_box.height)])

        #print(socket)
        self.set_output_socket(socket)

        if socket is None:
            return

       #self.output_socket = socket

        if self.input_socket is not None:
            self.input_socket.bind_with(socket, self)

        self.start_box.move_to(socket.x, socket.y)

    def resize(self, w: int, h: int):
        super().resize(w, h)
        self.end_box.move_to(w, h)

        if self.input_socket is not None:
            self.input_socket.unbind()
        #self.input_socket = None

        # try to connect
        # can connect to input
        socket = self.cmp.find_input_socket_by_coord([
            (self.width,                      self.height),
            (self.width + self.end_box.width, self.height),
            (self.width,                      self.height + self.end_box.height),
            (self.width + self.end_box.width, self.height + self.end_box.height)])

        #print(socket)

        self.set_input_socket(socket)

        if socket is None:
            return

        # disconnect other connection from socket if it was in it
        if socket.output_socket is not None:
            other_connection, part = self.cmp.find_connection_by_coord(socket.x + socket.size / 2, socket.y + socket.size / 2)
            if other_connection is not None and part == EPE.END:
                other_connection.disconnect_from_input()

        if self.output_socket is not None:
            socket.bind_with(self.output_socket, self)

        self.end_box.move_to(socket.x, socket.y)

    def get_start_box(self)->SimBox:
        return self.start_box

    def get_end_box(self)->SimBox:
        return self.end_box

    def get_start_socket(self)->OutputSocket:
        return self.output_socket

    def get_end_socket(self)->InputSocket:
        return self.input_socket

    def set_output_socket(self, socket: OutputSocket):
        self.output_socket = socket
        if self.input_socket is None and self.output_socket is None:
            self.cmp.delete_connection(self)

    def set_input_socket(self, socket: InputSocket):
        self.input_socket = socket
        if self.input_socket is None and self.output_socket is None:
            self.cmp.delete_connection(self)

    def paint(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        painter.set_pen_width(3)

        # start arrow
        if self.output_socket is not None:
            painter.set_pen_colour(0, 255, 0)
            #self.x = self.output_socket.x
            #self.y = self.output_socket.y
            self.start_box.x = self.output_socket.x
            self.start_box.y = self.output_socket.y
            #self.x, self.y = self.output_socket.x, self.output_socket.y
        else:
            painter.set_pen_colour(255, 0, 0)

        x1 = x_indent + self.start_box.x
        y1 = y_indent + self.start_box.y
        #painter.draw_circle(x1 + 5, y1 + 5, 3)
        painter.draw_line(x1, y1 + 2, x1 + 6, y1 + 5)
        painter.draw_line(x1, y1 + 8, x1 + 6, y1 + 5)

        # end arrow
        if self.input_socket is not None:
            painter.set_pen_colour(0, 255, 0)
            #self.width = self.input_socket.x
            #self.height = self.input_socket.y

            self.end_box.x = self.input_socket.x
            self.end_box.y = self.input_socket.y
            #self.width, self.height = self.input_socket.x, self.input_socket.y
        else:
            painter.set_pen_colour(255, 0, 0)

        x2 = x_indent + self.end_box.x
        y2 = y_indent + self.end_box.y
        #painter.draw_circle(x2 + 5, y2 + 5, 3)
        painter.draw_line(x2, y2 + 2, x2 + 6, y2 + 5)
        painter.draw_line(x2, y2 + 8, x2 + 6, y2 + 5)

        # line
        painter.set_pen_width(1)
        painter.set_pen_colour(0, 0, 0)
        painter.draw_line(x1 + 4, y1 + 4, x2 + 4, y2 + 4)

    def in_element(self, x: int, y: int) -> EPE:
        if self.start_box.in_element(x, y) != EPE.NONE:
            return EPE.START
        if self.end_box.in_element(x, y) != EPE.NONE:
            return EPE.END

        return EPE.NONE

    def disconnect_from_input(self):
        # depend of socket position

        self.width, self.height = self.end_box.x, self.end_box.y

        dx, dy = -10, 0
        self.resize(self.width + dx, self.height + dy)
        if self.input_socket is not None:
            self.input_socket.unbind()
            self.input_socket = None
