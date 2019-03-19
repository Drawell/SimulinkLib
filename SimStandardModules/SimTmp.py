from SimElement.sim_base_class import SimBaseClass, paint_func
from SimPainter.sim_painter import SimPainter


class SimTmp(SimBaseClass):
    def __init__(self, x: int, y: int, **kwargs):
        super(SimTmp, self).__init__(x, y, kwargs)

    @staticmethod
    def get_name() -> str:
        return 'SimSim'

    def make_step(self, time: float):
        pass

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        painter.draw_rectangle(x + 1, y + 1, w - 2, h - 2)
        painter.draw_text(x + w/10, y + h/2 + h / 5, "Hi!", int(min(h*2/3, w * 2/3)))

    @paint_func
    def paint(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        SimTmp.paint_base(painter, self.x + x_indent, self.y + y_indent, self.width, self.height)
        painter.draw_text(self.x + x_indent, self.y + y_indent + self.height + self.font, self.name, self.font)