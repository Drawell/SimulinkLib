from SimElement import SimBaseClass, paint_func
from SimPainter.sim_painter import SimPainter


class SimConst(SimBaseClass):
    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x, y, kwargs)
        self.value = 0
        self.value_socket = self.new_output_socket()

    @staticmethod
    def get_name()->str:
        return 'Const'

    def make_step(self, time: float):
        pass

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        painter.draw_rectangle(x + 1, y + 1, w - 2, h - 2)
        painter.draw_text(x + w / 10, y + h * 1/2, 'Const', int(min(h * 2 / 3, w * 1 / 5)))

    @paint_func
    def paint(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        x = x_indent + self.x
        y = y_indent + self.y
        painter.draw_rectangle(x + 1, y + 1, self.width - 2, self.height - 2)
        painter.draw_text(x + self.width / 10, y + self.height * 1/2,
                          str(self.value), int(min(self.height * 2 / 3, self.font)))
        painter.draw_text(self.x + x_indent, self.y + y_indent + self.height + self.font, self.name, self.font)
