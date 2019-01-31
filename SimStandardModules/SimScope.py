from sim_base_class import SimBaseClass
import os


class SimScope(SimBaseClass):
    def __init__(self, x: int, y: int,):
        super().__init__(x, y)

    def make_step(self):
        pass

    @staticmethod
    def get_img_path()->str:
        return os.path.join(os.path.dirname(__file__), 'Images', 'sim_scope.png') #'SimStandardModules',

    @staticmethod
    def get_name()->str:
        return 'SimScope'
