from PySimCore import SimBaseClass, paint_func, sim_property, SimPainter
from random import randint


class SimConst(SimBaseClass):
    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x, y, kwargs)

        if 'value' in kwargs:
            self.value = int(kwargs['value'])
        else:
            self.value = randint(1, 255)

        self.output = self.new_output_socket()

    @sim_property
    def value(self):
        pass

    @staticmethod
    def get_name()->str:
        return 'Const'

    def init_simulation(self, context):
        super().init_simulation(context)

    def iterate(self, time: float, context):
        self.output.put_value(self.value)

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        painter.draw_rectangle(x + 1, y + 1, w - 2, h - 2)
        painter.draw_text(x + w / 10, y + h * 1/2, 'Const', int(min(h * 2 / 3, w * 1 / 5)))

    @paint_func
    def paint(self, painter: SimPainter, x: float = 0, y: float = 0, scale: float = 1):
        painter.draw_rectangle(x + 1, y + 1, self.width - 2, self.height - 2)
        painter.draw_text(x + self.width / 10, y + self.height * 1/2,
                          str(self.value), int(min(self.height * 2 / 3, self.font)))
        #painter.draw_text(x, y + self.height + self.font, self.name, self.font)
