from PySimCore import SimBaseClass, ElementPartEnum as EPE, CheckExceptionEnum as CHE, SimConnection, SimBox, Socket
from PySimCore import SimPainter, OutputSocket, InputSocket
import xml.etree.ElementTree as xml


class Environment(SimBaseClass):
    def __init__(self, x: int, y: int, width: int, height: int, name: str):
        super().__init__(0, 0, {'width': int(width), 'height': int(height), 'name': name})
        self.present_elements = {}
        self.present_connections = []
        self.run_queue = []
        self.target_x = 0
        self.target_y = 0

    def make_step(self, time: float):
        pass

    def move_to(self, x: int, y: int):
        super().move_to(min(x, 0), min(y, 0))

    @staticmethod
    def get_name() -> str:
        return 'Environment'

    def check(self, context):
        check_result = {CHE.VARIABLE_REQUIRED: [], CHE.DISCONNECTED_SOCKET: [], CHE.INFINITIVE_CYCLE: []}

        #check for exceptions
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

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        pass

    def paint(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
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

        output_socket.bind_with(input_socket)
        connection = SimConnection(self, output_socket.x, output_socket.y, input_socket.x, input_socket.y)
        connection.set_output_socket(output_socket)
        connection.set_input_socket(input_socket)
        self.add_connection(connection)
        return True

    def add_connection(self, connection: SimConnection):
        self.present_connections.append(connection)
        self.dirty = True

    def try_to_connect(self, sender: SimConnection):
        # connect input socket
        #print("start connection")
        box = sender.end_box
        x, y = self.x, self.y
        input_socket = self.find_input_socket_by_coord(
            [(box.x + x, box.y + y), (box.x + box.width + x, box.y + y),
             (box.x + x, box.y + box.height + y), (box.x + box.width + x, box.y + box.height + y)])

        #print('input socket: ', input_socket)
        # connect output socket

        box = sender.start_box
        output_socket = self.find_output_socket_by_coord(
            [(box.x + x, box.y + y), (box.x + box.width + x, box.y + y),
             (box.x + x, box.y + box.height + y), (box.x + box.width + x, box.y + box.height + y)])

        #print('output socket: ', output_socket)

        if output_socket is None:  # start is disconnected
            if sender.get_end_socket() is not None:  # end connected -> unbinding
                sender.get_end_socket().unbind()
            sender.set_output_socket(None)
        else:
            # start is connected -> set start socket
            sender.set_output_socket(output_socket)

        if input_socket is None:  # end is dis connected
            if sender.input_socket is not None:  # but steel exists -> unbinding
                sender.get_end_socket().unbind()
                sender.set_input_socket(None)
        else:
            sender.set_input_socket(input_socket)
            # check for already connected connections
            for connection in self.present_connections:
                if connection.end_box.in_element(input_socket.x, input_socket.y) != EPE.NONE \
                        and connection is not sender:
                        connection.end_socket = None
                        connection.end_box.move_to(connection.end_box.x - 10, connection.end_box.y)

        if input_socket is not None and output_socket is not None:
            # start is connected and end is connected -> binding
            input_socket.bind_with(output_socket)

        print('Connection: Start socket: ', sender.get_start_socket(), '; End socket: ', sender.get_end_socket())

    def get_element_by_coord(self, x, y):
        for element in self.present_elements.values():
            part = element.in_element(x - self.x, y - self.y)
            if part != EPE.NONE:
                return element, part

        for connection in self.present_connections:
            if connection.start_box.in_element(x - self.x, y - self.y) != EPE.NONE:
                return connection, connection.start_box
            elif connection.end_box.in_element(x - self.x, y - self.y) != EPE.NONE:
                return connection, connection.end_box

        socket = self.find_output_socket_by_coord([(x, y)])
        if socket is not None:
            return socket, None

        socket = self.find_input_socket_by_coord([(x, y)])
        if socket is not None:
            return socket, None

        return None, None

    def get_element_by_name(self, name: str):
        if name in self.present_elements.keys():
            return self.present_elements[name]
        else:
            return None

    def get_socket(self, element_name, socket_index)-> Socket:
        element = self.get_element_by_name(element_name)

        if element is None:
            return None

        socket = element.get_input_socket(socket_index)
        if socket is None:
            socket = element.get_output_socket(socket_index)

        return socket

    def find_input_socket_by_coord(self, list_of_coord: list):
        for element in self.present_elements.values():
            for socket in element.input_sockets_iter():
                for x, y in list_of_coord:
                    if socket.in_element(x - self.x, y - self.y) != EPE.NONE:
                        return socket
        return None

    def find_output_socket_by_coord(self, list_of_coord: list):
        for element in self.present_elements.values():
            for socket in element.output_sockets_iter():
                for x, y in list_of_coord:
                    if socket.in_element(x - self.x, y - self.y) != EPE.NONE:
                        return socket
        return None

    def save_to_xml(self, parent):
        env_xml = xml.SubElement(parent, 'Environment')

        props = xml.SubElement(env_xml, 'Properties')
        for key, value in self.properties.items():
            prop = xml.SubElement(props, key)
            prop.text = str(value)

        for element in self.present_elements.values():
            element.save_to_xml(env_xml)

        for connection in self.present_connections:
            connection.save_to_xml(env_xml)

    #@staticmethod
    #def parse_xml(parent):

