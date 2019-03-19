from SimElement import SimBaseClass, paint_func
from SimPainter.sim_painter import SimPainter


class SimPlus(SimBaseClass):
    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x, y, kwargs)
        self.output = self.new_output_socket()
        self.inputs = []
        self.inputs.append(self.new_input_socket())
        self.inputs.append(self.new_input_socket())

    @staticmethod
    def get_name()->str:
        return 'Plus'

    def make_step(self, time: float):
        pass

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        painter.set_pen_width(1)
        painter.draw_rectangle(x + 1, y + 1, w - 2, h - 2)
        painter.set_pen_width(3)
        painter.draw_line(x + w/2, y + h/6, x + w/2, y + h * 5/6)
        painter.draw_line(x + w/6, y + h/2, x + w * 5/6, y + h/2)

    @paint_func
    def paint(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        SimPlus.paint_base(painter, self.x + x_indent, self.y + y_indent, self.width, self.height)
        painter.draw_text(self.x + x_indent, self.y + y_indent + self.height + self.font, self.name, self.font)
