from PySimCore import SimBaseClass, paint_func, sim_property, SimPainter


class SimMultiply(SimBaseClass):
    def __init__(self, x: int, y: int, **kwargs):
        self.inputs = []
        super().__init__(x, y, kwargs)
        self.output = self.new_output_socket()
        self.set_sockets_to_positions()

    def update(self, new_properties: dict):
        if 'signs' not in new_properties:
            self.signs = '**'
        else:
            self.signs = ''
            for sign in new_properties['signs']:
                if sign in ['/', '*']:
                    self.signs += sign

        for i in range(len(self.signs) - len(self.inputs)):
            self.inputs.append(self.new_input_socket())
        for i in range(len(self.inputs) - len(self.signs)):
            self.delete_socket(self.inputs.pop())

    @sim_property
    def signs(self):
        pass

    @staticmethod
    def get_name()->str:
        return 'Multiply'

    def init_simulation(self, context):
        pass

    def iterate(self, time: float, context):
        total_sum = 1
        for i, socket in enumerate(self.inputs):
            if self.signs[i] == '*':
                total_sum *= socket.get_value()
            elif self.signs[i] == '/':
                total_sum /= socket.get_value()

        self.output.put_value(total_sum)

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        painter.set_pen_width(1)
        painter.draw_rectangle(x + 1, y + 1, w - 2, h - 2)
        painter.draw_text(x + w / 3, y + h*4/5, '*', 25)

    @paint_func
    def paint(self, painter: SimPainter, x: float = 0, y: float = 0, scale: float = 1):
        painter.set_pen_width(1)
        painter.draw_rectangle(x + 1, y + 1, self.width - 2, self.height - 2)
        for i, sign in enumerate(self.signs):
            painter.draw_text(x + self.inputs[i].x_in_parent + 14,
                              y + self.inputs[i].y_in_parent + 10, sign, self.font)