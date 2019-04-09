from PySimCore import SimBaseClass, sim_property, paint_func, SimPainter, SocketPositionEnum as SPE


class SimAdd(SimBaseClass):
    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x, y, kwargs)
        self.output = self.new_output_socket()

        self.sings = kwargs['signs'] if 'signs' in kwargs else '++'

        self.inputs = []
        for sign in self.sings:
            self.inputs.append(self.new_input_socket())

        self.set_sockets_to_positions()

    @sim_property
    def sings(self):
        pass

    @staticmethod
    def get_name()->str:
        return 'Add'

    def init_simulation(self, context):
        super().init_simulation(context)

    def iterate(self, time: float, context):
        sum = 0
        for i, input in enumerate(self.inputs):
            if self.sings[i] == '+':
                sum += input.get_value()
            elif self.sings[i] == '-':
                sum -= input.get_value()

        self.output.put_value(sum)

    def set_sockets_to_positions(self):
        super().set_sockets_to_positions()
        #self.inputs[0].set_to_pos(self.width / 2 - 5, -10)

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        painter.set_pen_width(1)
        painter.draw_rectangle(x + 1, y + 1, w - 2, h - 2)
        painter.set_pen_width(3)
        painter.draw_line(x + w/2, y + h/6, x + w/2, y + h * 5/6)
        painter.draw_line(x + w/6, y + h/2, x + w * 5/6, y + h/2)

    @paint_func
    def paint(self, painter: SimPainter, x: float = 0, y: float = 0, scale: float = 1):
        #SimAdd.paint_base(painter, x, y, self.width, self.height)
        #painter.draw_text(x, y + self.height + self.font, self.name, self.font)
        painter.set_pen_width(1)
        painter.draw_rectangle(x + 1, y + 1, self.width - 2, self.height - 2)
        for i, sign in enumerate(self.sings):
            painter.draw_text(x + self.inputs[i].x_in_parent + 14, y + self.inputs[i].y_in_parent + 10, sign, self.font)
