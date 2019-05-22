from PySimCore import SimBaseClass, sim_property, paint_func, SimPainter
import math


class SSin(SimBaseClass):
    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x, y, kwargs)
        self.input = self.new_input_socket()
        self.output = self.new_output_socket()
        self.set_sockets_to_positions()

    @staticmethod
    def get_name() -> str:
        return 'Sinus'

    def init_simulation(self, context):
        pass

    def iterate(self, time: float, context):
        self.output.put_value(math.sin(self.input.get_value()))

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        painter.set_pen_width(1)
        painter.draw_rectangle(x + 1, y + 1, w - 2, h - 2)
        painter.draw_text(x + w / 2 - 10, y + h / 2 + 10, 'sin', 15)

    @paint_func
    def paint(self, painter: SimPainter, x: float = 0, y: float = 0, scale: float = 1):
        painter.set_pen_width(1)
        painter.draw_rectangle(x + 1, y + 1, self.width - 2, self.height - 2)
        painter.draw_text(x + self.width / 2 - 10, y + self.height / 2 + 10, 'sin', 15)