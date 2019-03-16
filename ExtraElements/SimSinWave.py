from SimElement.sim_base_class import SimBaseClass
from SimPainter.sim_painter import SimPainter


class SimSinWave(SimBaseClass):
    def __init__(self, x: int, y: int, amplitude: float = 0, phase: float = 0, **kwargs):
        super().__init__(x, y, kwargs)
        self.amplitude = amplitude
        self.phase = phase

    @staticmethod
    def get_name()->str:
        return 'Sin Wave'

    def make_step(self, time: float):
        pass

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        painter.draw_rectangle(x + 1, y + 1, w - 2, h - 2)
        painter.draw_line(x + 5, y + h / 2, x + w - 5, y + h / 2)
        painter.draw_line(x + w / 5, y + 5, x + w / 5, y + h - 5)
        painter.draw_curve(x + w / 5, y + h / 2, x + 1.5 * w / 5, y + 5,
                           x + 2.5 * w / 5, y + 5, x + 3 * w / 5, y + h / 2)
        painter.draw_curve(x + 3 * w / 5, y + h / 2, x + 3.5 * w / 5, y + h - 10,
                           x + 4.5 * w / 5, y + h - 10, x + w - 2, y + h / 2)

    def paint(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        SimSinWave.paint_base(painter, self.x + x_indent, self.y + y_indent, self.width, self.height)
        painter.draw_text(self.x + x_indent, self.y + y_indent + self.height + self.font, self.name, self.font)
