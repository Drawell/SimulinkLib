import os
import importlib.util
from importlib import import_module
from environment import Environment
from env_manager import EnvManager
from SimStandardModules.SimTmp import SimTmp


class A:
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return self.s


class B:
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return 'i am ' + self.s


s = B.__name__
print(s)
'''
path = os.path.join(os.path.dirname(__file__), 'SimStandardModules')
env = Environment()
manager = EnvManager(env)
manager.import_classes_from_dir(path)
#manager.add_class_by_name('SimTmp')
imported_class = manager.imported_classes['SimTmp']
el = imported_class(0, 0)
'''
'''
def import_from_dir(path: str):
    #os.path.isfile
    files = os.listdir(path)
    error = []
    for name in files:
        module_path = os.path.join(path, name)
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
            d[class_name] = getattr(module, class_name)
        except AttributeError:
            error.append("some import error in module %s" % name)

    return error


path = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'SimStandardModules')

error = import_from_dir(path)
print(error)
cls = d['SimTmp']('asd')
print(cls)

'''

