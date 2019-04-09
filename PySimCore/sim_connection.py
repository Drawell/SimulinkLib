from PySimCore import ElementPartEnum as EPE, SimBox, InputSocket, OutputSocket, SimPainter
import xml.etree.ElementTree as xml


class SimConnection(SimBox):
    def __init__(self, env, x_start: int, y_start: int, x_end, y_end):
        super().__init__(x_start, y_start, x_end, y_end)
        self.env = env
        self.start_box = SimBox(x_start, y_start, 8, 8)
        self.end_box = SimBox(x_end, y_end, 8, 8)
        self.output_socket = None
        self.input_socket = None

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

    def set_input_socket(self, socket: InputSocket):
        self.input_socket = socket

    def paint(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        painter.set_pen_width(3)

        # start arrow
        if self.output_socket is not None:
            painter.set_pen_colour(0, 255, 0)
            self.start_box.x = self.output_socket.x
            self.start_box.y = self.output_socket.y
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
            self.end_box.x = self.input_socket.x
            self.end_box.y = self.input_socket.y
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
        return EPE.NONED

    def save_to_xml(self, parent):
        connection_xml = xml.SubElement(parent, 'Connection')
        self.move_to(self.start_box.x, self.start_box.y)
        self.resize(self.end_box.x, self.end_box.y)
        super().save_to_xml(connection_xml)
        #start_box_xml = xml.SubElement(connection_xml, 'StartBox')
        #self.start_box.save_to_xml(start_box_xml)
        #end_box_xml = xml.SubElement(connection_xml, 'EndBox')
        #self.end_box.save_to_xml(end_box_xml)

        start_socket_xml = xml.SubElement(connection_xml, 'StartSocket')
        if self.input_socket is None:
            none_tag = xml.SubElement(start_socket_xml, 'None')
        else:
            name_xml = xml.SubElement(start_socket_xml, 'name')
            name_xml.text = self.output_socket.name
            index_xml = xml.SubElement(start_socket_xml, 'index')
            index_xml.text = str(self.output_socket.index)

        end_socket_xml = xml.SubElement(connection_xml, 'EndSocket')
        if self.input_socket is None:
            none_tag = xml.SubElement(end_socket_xml, 'None')
        else:
            name_xml = xml.SubElement(end_socket_xml, 'name')
            name_xml.text = self.input_socket.name
            index_xml = xml.SubElement(end_socket_xml, 'index')
            index_xml.text = str(self.input_socket.index)

    @staticmethod
    def parse_xml(element):
        pass