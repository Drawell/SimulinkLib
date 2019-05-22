from PySimCore import SimBaseClass, SimPainter, paint_func


class SimSinWave(SimBaseClass):
    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x, y, kwargs)
        #self.amplitude = amplitude
        #self.phase = phase

    @staticmethod
    def get_name()->str:
        return 'SinWave'

    def init_simulation(self, context):
        pass

    def iterate(self, time: float, context):
        pass

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        painter.draw_rectangle(x + 1, y + 1, w - 2, h - 2)
        painter.draw_line(x + 5, y + h / 2, x + w - 5, y + h / 2)
        painter.draw_line(x + w / 5, y + 5, x + w / 5, y + h - 5)
        painter.set_pen_width(2)
        painter.draw_curve(x + w / 5, y + h / 2, x + 1.5 * w / 5, y + 5,
                           x + 2.5 * w / 5, y + 5, x + 3 * w / 5, y + h / 2)
        painter.draw_curve(x + 3 * w / 5, y + h / 2, x + 3.5 * w / 5, y + h - 10,
                           x + 4.5 * w / 5, y + h - 10, x + w - 2, y + h / 2)

    @paint_func
    def paint(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        SimSinWave.paint_base(painter, self.x + x_indent, self.y + y_indent, self.width, self.height)
        painter.draw_text(self.x + x_indent, self.y + y_indent + self.height + self.font, self.name, self.font)
