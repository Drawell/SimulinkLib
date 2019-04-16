from PySimCore import SimBaseClass, sim_property, paint_func, SimPainter, RotationPositionEnum as SPE


class SimAdd(SimBaseClass):
    def __init__(self, x: int, y: int, **kwargs):
        self.inputs = []
        super().__init__(x, y, kwargs)
        self.output = self.new_output_socket()

        #for sign in self.signs:
        #    self.inputs.append(self.new_input_socket())

        self.set_sockets_to_positions()

    def update(self, new_properties: dict):
        if 'signs' not in new_properties:
            new_signs = '++'
        else:
            # fool protection
            new_signs = ''
            for sign in new_properties['signs']:
                if sign in ['-', '+']:
                    new_signs += sign

        self.signs = new_signs

        if len(self.signs) > len(self.inputs):   # add new sockets
            for i in range(len(self.signs) - len(self.inputs)):
                self.inputs.append(self.new_input_socket())
        elif len(self.signs) < len(self.inputs):  # delete sockets
            for i in range(len(self.inputs) - len(self.signs)):
                self.delete_socket(self.inputs.pop())

    @sim_property
    def signs(self):
        pass

    @staticmethod
    def get_name()->str:
        return 'Add'

    def init_simulation(self, context):
        super().init_simulation(context)

    def iterate(self, time: float, context):
        sum = 0
        for i, input in enumerate(self.inputs):
            if self.signs[i] == '+':
                sum += input.get_value()
            elif self.signs[i] == '-':
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
        painter.draw_line(x + w/2, y + h/5, x + w/2, y + h * 4/5)
        painter.draw_line(x + w/5, y + h/2, x + w * 4/5, y + h/2)

    @paint_func
    def paint(self, painter: SimPainter, x: float = 0, y: float = 0, scale: float = 1):
        #SimAdd.paint_base(painter, x, y, self.width, self.height)
        #painter.draw_text(x, y + self.height + self.font, self.name, self.font)
        painter.set_pen_width(1)
        painter.draw_rectangle(x + 1, y + 1, self.width - 2, self.height - 2)
        for i, sign in enumerate(self.signs):
            painter.draw_text(x + self.inputs[i].x_in_parent + 14, y + self.inputs[i].y_in_parent + 10, sign, self.font)
