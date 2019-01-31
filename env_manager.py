from typing import Dict
import importlib.util
import os
from sim_base_class import SimBaseClass
from environment import Environment

## @package env_maneger
#  Содержит импортированные классы, которые можно добавить.
#
# Добавляет в среду екземпляры классов по имени.


## Содержит импортированные классы, которые можно добавить
#
# Добавляет в среду екземпляры классов по имени.
# Может быть объеденить со средой?
class EnvManager:
    def __init__(self, environment: Environment):
        self.imported_classes = {}  # : Dict[SimBaseClass]
        self.environment = environment

    def import_classes_from_dir(self, dir_path):
        files = os.listdir(dir_path)
        error = []
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
                error.append("some import error in module %s" % name)
                continue

            try:
                self.imported_classes[class_name] = getattr(module, class_name)
            except AttributeError:
                error.append("some import error in module %s" % name)

        return error

    def add_class_by_name(self, class_name: str, x: int = 0, y: int = 0):
        if class_name in self.imported_classes.keys():
            element = self.imported_classes[class_name](x, y)
            self.environment.add_element(element)
