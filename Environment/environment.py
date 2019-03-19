from SimElement.sim_base_class import SimBaseClass
from SimElement.element_part_enum import ElementPartEnum as EPE
from SimElement.sim_connection import SimConnection
from SimElement.sim_box import SimBox
from SimPainter.sim_painter import SimPainter


## @package environment
#  Среда. В ней будет все
#
#

## Среда. В ней будет все
class Environment(SimBaseClass):
    def __init__(self, x: int, y: int):
        super().__init__(0, 0, {})
        self.present_elements = []
        self.present_connections = []
        self.target_x = 0
        self.target_y = 0

    def make_step(self, time: float):
        pass

    def move_to(self, x: int, y: int):
        super().move_to(min(x, 0), min(y, 0))

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        pass

    def paint(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        painter.clear()
        for element in self.present_elements:
            element.paint(painter, self.x, self.y, scale)
        for connection in self.present_connections:
            connection.paint(painter, self.x, self.y, scale)

    def add_element(self, element: SimBaseClass):
        self.present_elements.append(element)
        self.width = max(element.x + element.width, self.width)
        self.height = max(element.y + element.height, self.height)
        self.dirty = True

    def add_connection(self, connection: SimConnection):
        self.present_connections.append(connection)
        self.dirty = True

    def try_to_connect(self, sender: SimConnection):
        # connect input socket
        print("start connection")
        box = sender.end_box
        input_socket = self.find_input_socket_by_coord(
            [(box.x, box.y), (box.x + box.width, box.y),
             (box.x, box.y + box.height), (box.x + box.width, box.y + box.height)])

        print('input socket: ', input_socket)

        # connect output socket
        box = sender.start_box
        output_socket = self.find_output_socket_by_coord(
            [(box.x, box.y), (box.x + box.width, box.y),
             (box.x, box.y + box.height), (box.x + box.width, box.y + box.height)])

        print('output socket: ', output_socket)

        if output_socket is None:  # start is disconnected
            if sender.get_end_socket() is not None:  # end connected -> unbinding
                sender.get_end_socket().unbind()
            sender.set_start_socket(None)
        else:
            # start is connected -> set start socket
            sender.set_start_socket(output_socket)

        if input_socket is None:  # end is dis connected
            if sender.end_socket is not None:  # but steel exists -> unbinding
                sender.get_end_socket().unbind()
                sender.set_end_socket(None)
        else:
            sender.set_end_socket(input_socket)

        if input_socket is not None and output_socket is not None:
            # start is connected and end is connected -> binding
            input_socket.bind_with(output_socket)

        print('Connection: Start socket: ', sender.get_start_socket(), '; End socket: ', sender.get_end_socket())

    def disconnect_from_end(self, sender: SimConnection):
        pass

    def disconnect_from_start(self, sender: SimConnection):
        pass

    def get_element_by_coord(self, x, y):
        for element in self.present_elements:
            part = element.in_element(x - self.x, y - self.y)
            if part != EPE.NONE:
                return element, part

        for connection in self.present_connections:
            if connection.start_box.in_element(x - self.x, y - self.y) != EPE.NONE:
                return connection, connection.start_box
            elif connection.end_box.in_element(x - self.x, y - self.y) != EPE.NONE:
                return connection, connection.end_box

        socket = self.find_output_socket_by_coord([(x - self.x, y - self.y)])
        if socket is not None:
            return socket, None

        socket = self.find_input_socket_by_coord([(x - self.x, y - self.y)])
        if socket is not None:
            return socket, None

        return None, None

    def find_input_socket_by_coord(self, list_of_coord: list):
        for element in self.present_elements:
            for socket in element.input_sockets_iter():
                for x, y in list_of_coord:
                    if socket.in_element(x - self.x, y - self.y) != EPE.NONE:
                        return socket
        return None

    def find_output_socket_by_coord(self, list_of_coord: list):
        for element in self.present_elements:
            for socket in element.output_sockets_iter():
                for x, y in list_of_coord:
                    if socket.in_element(x - self.x, y - self.y) != EPE.NONE:
                        return socket
        return None