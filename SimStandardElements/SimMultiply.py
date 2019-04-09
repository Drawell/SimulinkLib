from PySimCore import SimBaseClass, paint_func, sim_property, SimPainter


class SimMultiply(SimBaseClass):
    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x, y, kwargs)

    @sim_property
    def value(self):
        pass

    @staticmethod
    def get_name()->str:
        return 'Multiply'

    def init_simulation(self, context):
        super().init_simulation(context)

    def iterate(self, time: float, context):
        pass

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        painter.draw_rectangle(x + 1, y + 1, w - 2, h - 2)

    @paint_func
    def paint(self, painter: SimPainter, x: float = 0, y: float = 0, scale: float = 1):
        painter.draw_rectangle(x + 1, y + 1, self.width - 2, self.height - 2)
