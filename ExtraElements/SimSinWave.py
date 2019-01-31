from sim_base_class import SimBaseClass
import os


class SimSinWave(SimBaseClass):
    def __init__(self, x: int, y: int, amplitude: float = 0, phase: float = 0):
        super().__init__(x, y)
        self.amplitude = amplitude
        self.phase = phase

    @staticmethod
    def get_img_path()->str:
        return os.path.join(os.path.dirname(__file__), 'Images', 'SinWave.png') #'SimStandardModules',

    @staticmethod
    def get_name()->str:
        return 'SimSinWave'