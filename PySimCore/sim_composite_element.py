from PySimCore import SimBaseClass, ElementPartEnum as EPE, CheckExceptionEnum as CHE, SimConnection, SimBox, Socket

from PySimCore import SimPainter, OutputSocket, InputSocket
from typing import Union
import xml.etree.ElementTree as xml


class SimCompositeElement(SimBaseClass):
    def __init__(self, width: int, height: int, name: str):
        super().__init__(0, 0, {'width': int(width), 'height': int(height), 'name': name})
        self.present_elements = {}
        self.present_connections = []
        self.run_queue = []
        self.target_x = 0
        self.target_y = 0

    def move_to(self, x: int, y: int):
        super().move_to(min(x, 0), min(y, 0))

    @staticmethod
    def get_name() -> str:
        return 'Environment'

    def check(self, context):
        check_result = {CHE.VARIABLE_REQUIRED: [], CHE.DISCONNECTED_SOCKET: [], CHE.INFINITIVE_CYCLE: []}

        # check for exceptions
        for element in self.present_elements.values():
            for key in check_result:
                element_check_result = element.check(context)
                if key in element_check_result.keys():
                    check_result[key].extend(element_check_result[key])

        return check_result

    def init_simulation(self, context):
        self.run_queue.clear()
        for element in self.present_elements.values():
            self.run_queue.append(element)
            element.set_sockets_unchecked()
            element.dirty = False

        position = 0
        while position < len(self.present_elements.values()):
            was_changes = False
            #  element need to run previous element. Push it back
            if CHE.UNCHECKED_SOCKET in self.run_queue[position].check(context).keys():
                element = self.run_queue.pop(position)

                if element.dirty and not was_changes:  # element
                    raise Exception('Infinitive cycle!')

                element.dirty = True
                self.run_queue.append(element)
            else:  # all ok
                was_changes = True
                self.run_queue[position].dirty = True
                position += 1
                # clean up all rest elements
                for i in range(len(self.run_queue) - position):
                    self.run_queue[i + position].dirty = False

        for idx in range(len(self.run_queue)):
            self.run_queue[idx].init_simulation(context)

    def iterate(self, time: float, context):
        for idx in range(len(self.run_queue)):
            self.run_queue[idx].iterate(time, context)

    def get_local_variables(self)-> list:
        result = []
        for element in self.present_elements.values():
            result.extend(element.get_local_variables())
        return result

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        pass

    def paint(self, painter: SimPainter, x: float = 0, y: float = 0, scale: float = 1):
        pass

    def paint_full(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        painter.clear()
        for element in self.present_elements.values():
            element.paint(painter, self.x, self.y, scale)
        for connection in self.present_connections:
            connection.paint(painter, self.x, self.y, scale)

    def add_element(self, element: SimBaseClass):
        if element.name is None:
            raise Exception('Not named_element!')
        if element.name in self.present_elements.keys():
            raise Exception('Name already exists!')

        self.present_elements[element.name] = element
        self.width = max(element.x + element.width, self.width)
        self.height = max(element.y + element.height, self.height)
        self.dirty = True

    def connect(self, first_element: SimBaseClass, output_socket: OutputSocket,
                second_element: SimBaseClass, input_socket: InputSocket):
        if first_element not in self.present_elements.values() \
                or second_element not in self.present_elements.values() \
                or output_socket is None or input_socket is None:
            return False

        connection = SimConnection(self, output_socket.x, output_socket.y, input_socket.x, input_socket.y)
        connection.set_output_socket(output_socket)
        connection.set_input_socket(input_socket)
        output_socket.bind_with(input_socket, connection)
        self.add_connection(connection)
        return True

    def add_connection(self, connection: SimConnection):
        self.present_connections.append(connection)
        self.dirty = True

    def delete_connection(self, connection: SimConnection):
        if connection in self.present_connections:
            self.present_connections.remove(connection)

    def get_element_by_name(self, name: str):
        if name in self.present_elements.keys():
            return self.present_elements[name]
        else:
            return None

    def get_socket(self, element_name, socket_index)-> Union[Socket, None]:
        element = self.get_element_by_name(element_name)

        if element is None:
            return None

        socket = element.get_input_socket(socket_index)
        if socket is None:
            socket = element.get_output_socket(socket_index)

        return socket

    def find_element_by_coord(self, x, y)-> tuple:
        for element in self.present_elements.values():
            part = element.in_element(x, y)
            if part != EPE.NONE:
                return element, part

        return None, None

    def find_connection_by_coord(self, x, y)-> tuple:
        for connection in self.present_connections:
            part = connection.in_element(x, y)
            if part != EPE.NONE:
                return connection, part

        return None, None

    def find_input_socket_by_coord(self, list_of_coord: list)-> Union[InputSocket, None]:
        for element in self.present_elements.values():
            for socket in element.input_sockets_iter():
                for x, y in list_of_coord:
                    if socket.in_element(x, y) != EPE.NONE:
                        return socket
        return None

    def find_output_socket_by_coord(self, list_of_coord: list)-> Union[OutputSocket, None]:
        for element in self.present_elements.values():
            for socket in element.output_sockets_iter():
                for x, y in list_of_coord:
                    if socket.in_element(x, y) != EPE.NONE:
                        return socket
        return None

    def find_anything_by_coord(self, x, y) -> tuple:
        something, part = self.find_element_by_coord(x, y)
        if something is not None:
            return something, part

        something, part = self.find_connection_by_coord(x, y)
        if something is not None:
            return something, part

        something = self.find_output_socket_by_coord([(x, y)])
        if something is not None:
            return something, EPE.NONE

        something = self.find_input_socket_by_coord([(x, y)])
        if something is not None:
            return something, EPE.NONE

        return None, None
