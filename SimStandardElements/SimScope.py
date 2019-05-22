from PySimCore import SimBaseClass, paint_func, SimPainter
import matplotlib.pyplot as plt


class SimScope(SimBaseClass):
    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x, y, kwargs)
        self.time = []
        self.values = []
        self.input = self.new_input_socket()

    @staticmethod
    def get_name()->str:
        return 'SimScope'

    def init_simulation(self, context):
        super().init_simulation(context)
        self.time = []
        self.values = []

    def iterate(self, time: float, context):
        self.time.append(time)
        value = float(self.input.get_value())
        self.values.append(value)

    def show(self):
        plt.plot(self.time, self.values)
        return super().show()

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        painter.draw_rectangle(x + 1, y + 1, w - 2, h - 2)
        painter.draw_rectangle(x + w / 8, y + h / 8, w - w / 4, h/3)

    @paint_func
    def paint(self, painter: SimPainter, x: float = 0, y: float = 0, scale: float = 1):
        SimScope.paint_base(painter, x, y, self.width, self.height)
        #painter.draw_text(x, y + self.height + self.font, self.name, self.font)
