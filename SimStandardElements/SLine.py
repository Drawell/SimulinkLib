from PySimCore import SimBaseClass, paint_func, sim_property, SimPainter


class SLine(SimBaseClass):
    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x, y, kwargs)
        self.output = self.new_output_socket()
        self.set_sockets_to_positions()

    def update(self, new_properties: dict):
        if 'slope_coefficient' not in new_properties:
            self.slope_coefficient = 1
        else:
            self.slope_coefficient = float(new_properties['slope_coefficient'])

        if 'shift_coefficient' not in new_properties:
            self.shift_coefficient = 0
        else:
            self.shift_coefficient = float(new_properties['shift_coefficient'])

    @sim_property
    def slope_coefficient(self):
        pass

    @sim_property
    def shift_coefficient(self):
        pass

    @staticmethod
    def get_name()->str:
        return 'Line func'

    def init_simulation(self, context):
        pass

    def iterate(self, time: float, context):
        self.output.put_value(self.slope_coefficient * time + self.shift_coefficient)

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        painter.set_pen_width(1)
        painter.draw_rectangle(x + 1, y + 1, w - 2, h - 2)
        painter.draw_line(x + w / 5, y + h / 2, x + w * 4/5, y + h / 2)
        painter.draw_line(x + w / 5, y + h / 7, x + w / 5, y + h * 6/7)
        painter.set_pen_width(2)
        painter.draw_line(x + w / 5, y + h * 4/ 5, x + w * 4/5, y + h / 5)

    @paint_func
    def paint(self, painter: SimPainter, x: float = 0, y: float = 0, scale: float = 1):
        painter.set_pen_width(1)
        painter.draw_rectangle(x + 1, y + 1, self.width - 2, self.height - 2)
        painter.draw_rectangle(x + 1, y + 1, self.width - 2, self.height - 2)
        painter.draw_line(x + self.width / 5, y + self.height / 2, x + self.width * 4/5, y + self.height / 2)
        painter.draw_line(x + self.width / 5, y + self.height / 7, x + self.width / 5, y + self.height * 6/7)
        painter.set_pen_width(2)
        painter.draw_line(x + self.width / 5, y + self.height * 4/5, x + self.width * 4/5, y + self.height / 5)
