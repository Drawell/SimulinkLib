import importlib.util
import os
from PySimCore import SimConnection, CheckExceptionEnum as CHE, SimBaseClass, SimCompositeElement, SimPainter, \
    OutputSocket, InputSocket
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

    def get_variable_list(self)-> list:
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

    def connect(self, first_element: SimBaseClass, output_socket: OutputSocket,
                second_element: SimBaseClass, input_socket: InputSocket):
        self.cmp.connect(first_element, output_socket, second_element, input_socket)

