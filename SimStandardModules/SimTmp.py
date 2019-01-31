import os.path
from sim_base_class import SimBaseClass

class SimTmp(SimBaseClass):
    def __init__(self, x: int, y: int):
        super(SimTmp, self).__init__(x, y)

    def make_step(self):
        pass

    @staticmethod
    def get_img_path()->str:
        return os.path.join(os.path.dirname(__file__), 'Images', 'simsimsim.png')

    @staticmethod
    def get_name()->str:
        return 'SimSim'