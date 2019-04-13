import importlib.util
import os
from PySimCore import SimConnection, CheckExceptionEnum as CHE, SimBaseClass, SimCompositeElement, SimPainter
import xml.etree.ElementTree as xml
import xml.etree.cElementTree as cxml

## @package env_maneger
#  Содержит импортированные классы, которые можно добавить.
#
# Добавляет в среду екземпляры классов по имени.


## Содержит импортированные классы, которые можно добавить
#
# Добавляет в среду екземпляры классов по имени.
# Может быть объеденить со средой?
class Environment:
    def __init__(self, main_element: SimCompositeElement = None):
        self.imported_classes = {}  # : Dict[SimBaseClass]
        self.names_counter = {}
        if main_element is not None:
            self.cmp = main_element
            self.cmp.name = 'MainEnvironment'
        else:
            self.cmp = SimCompositeElement(200, 200, name='MainEnvironment')

        self.old_env = None

    def resize(self, w: int, h: int):
        self.cmp.resize(w, h)

    def paint(self, painter: SimPainter):
        self.cmp.paint_full(painter)

    def get_variable_list(self):
        return self.cmp.get_local_variables()

    def check(self, context):
        check = self.cmp.check(context)

        #if CHE.VARIABLE_REQUIRED in check.keys
        #self.environment.init_simulation(context)

    def run_simulation(self, start_time: float, end_time: float, time_step: float, context: dict):
        self.check(context)

        self.cmp.init_simulation(context)

        while start_time <= end_time:
            self.cmp.iterate(start_time, context)
            start_time += time_step

    def import_classes_from_dir(self, dir_path):
        files = os.listdir(dir_path)
        for name in files:
            module_path = os.path.join(dir_path, name)
            if not os.path.isfile(module_path):
                continue

            class_name = name[:-3]  # cut .py

            try:
                spec = importlib.util.spec_from_file_location(class_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            except ImportError:
                raise Exception("some import error in module %s" % name)

            try:
                self.imported_classes[class_name] = getattr(module, class_name)
                self.names_counter[class_name] = 0
            except AttributeError:
                raise Exception("some import error in module %s" % name)

    def add_element_by_name(self, class_name: str, x: int = 0, y: int = 0):
        if class_name in self.imported_classes.keys():
            name = self.generate_name(class_name)
            element = self.imported_classes[class_name](x - self.cmp.x, y - self.cmp.y, name=name)
            self.cmp.add_element(element)

    def add_element(self, element: SimBaseClass):
            class_name = element.__class__.__name__
            element.name = self.generate_name(class_name)
            self.cmp.add_element(element)

    def generate_name(self, class_name: str):
        if class_name not in self.names_counter:
            # self.imported_classes[class_name] = element.__class__
            self.names_counter[class_name] = 0
        else:
            self.names_counter[class_name] += 1
        return class_name + '_' + str(self.names_counter[class_name])

    def add_number_for_name_generation(self, class_name: str, number: int):
        self.names_counter[class_name] = max(number, self.names_counter[class_name])

    '''
    def change_connection(self, sender: SimConnection):
        # connect input socket
        #print("start connection")
        box = sender.end_box
        x, y = self.composite_element.x, self.composite_element.y
        input_socket = self.composite_element.find_input_socket_by_coord(
            [(box.x + x, box.y + y), (box.x + box.width + x, box.y + y),
             (box.x + x, box.y + box.height + y), (box.x + box.width + x, box.y + box.height + y)])

        #print('input socket: ', input_socket)
        # connect output socket

        box = sender.start_box
        output_socket = self.composite_element.find_output_socket_by_coord(
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
            for connection in self.composite_element.present_connections:
                if connection.end_box.in_element(input_socket.x, input_socket.y) != EPE.NONE \
                        and connection is not sender:
                        connection.end_socket = None
                        connection.end_box.move_to(connection.end_box.x - 10, connection.end_box.y)

        if input_socket is not None and output_socket is not None:
            # start is connected and end is connected -> binding
            input_socket.bind_with(output_socket)

        #print('Connection: Start socket: ', sender.get_start_socket(), '; End socket: ', sender.get_end_socket())

    '''

    def disconnect(self, sender: SimConnection):
        pass

    # need to move

    def save_to_xml(self, file_path):
        root = xml.Element("root")
        main_env = xml.Element('MainEnvironment')
        root.append(main_env)
        self.cmp.save_to_xml(main_env)

        tree = xml.ElementTree(root)
        tree.write(file_path)

    def parse_xml(self, path):
        self.old_env = self.cmp
        tree = cxml.ElementTree(file=path)
        root = tree.getroot()
        for child in root:
            print(child.tag, child.attrib)
            if child.tag == "MainEnvironment":
                self.parse_main_env(child)
                #env_manager = EnvManager(env)

    def parse_main_env(self, main_env):
        env_xml = main_env[0]
        if env_xml.tag != 'Environment':
            raise Exception('Filed to parse xml')

        for child in env_xml:
            if child.tag == 'Properties':
                prop = Environment.parse_properties(child)
                x = int(prop['x'])
                y = int(prop['y'])
                w = int(prop['width'])
                h = int(prop['height'])
                name = prop['name']
                self.cmp = Environment(x, y, w, h, name)
            elif child.tag == 'Element':
                self.parse_element(child)
            elif child.tag == 'Connection':
                self.parse_connection(child)

    def parse_element(self, element):
        class_name = element.text.strip()

        if class_name not in self.imported_classes:
            raise Exception('Need to import class %s' % class_name)

        for prop_xml in element:
            if prop_xml.tag != 'Properties':
                raise Exception('Can not find properties for class %s' % class_name)

            prop = Environment.parse_properties(prop_xml)
            x = int(prop['x'])
            y = int(prop['y'])
            prop['width'] = int(prop['width'])
            prop['height'] = int(prop['height'])
            name = prop['name']
            self.add_number_for_name_generation(class_name, int(name[len(class_name) + 1:]))
            self.cmp.add_element(self.imported_classes[class_name](**prop))
            break

    def parse_connection(self, connection_xml):
        for element in connection_xml:
            if element.tag == 'SimBox':
                prop = Environment.parse_properties(element)
                x = int(prop['x'])
                y = int(prop['y'])
                w = int(prop['width'])
                h = int(prop['height'])
                connection = SimConnection(self.cmp, x, y, w, h)

            if element.tag == 'StartSocket':
                if element[0].tag != 'None':
                    prop = Environment.parse_properties(element)
                    name = prop['name']
                    index = int(prop['index'])
                    connection.output_socket = self.cmp.get_socket(name, index)

                    if connection.input_socket is not None:
                        connection.output_socket.bind_with(connection.input_socket)

            if element.tag == 'EndSocket':
                if element[0].tag != 'None':
                    prop = Environment.parse_properties(element)
                    name = prop['name']
                    index = int(prop['index'])
                    connection.input_socket = self.cmp.get_socket(name, index)

                    if connection.output_socket is not None:
                        connection.output_socket.bind_with(connection.input_socket)

        self.cmp.add_connection(connection)

    @staticmethod
    def parse_properties(parent):
        result = {}
        for prop in parent:
            print(prop.tag)
            result[prop.tag] = prop.text
        return result

