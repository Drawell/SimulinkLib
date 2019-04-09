from PySimCore import SimBaseClass, paint_func, sim_property, SimPainter


class SimSetVariable(SimBaseClass):
    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x, y, kwargs)
        self.var_name = kwargs['var_name'] if 'var_name' in kwargs else self.name
        self.input = self.new_input_socket()

    @sim_property
    def var_name(self):
        pass

    @staticmethod
    def get_name()->str:
        return 'SetVariable'

    def init_simulation(self, context):
        super().init_simulation(context)
        context[self.var_name] = []

    def iterate(self, time: float, context):
        context[self.var_name].append(self.input.get_value())

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        painter.draw_rectangle(x + 1, y + 1, w - 2, h - 2)

    @paint_func
    def paint(self, painter: SimPainter, x: float = 0, y: float = 0, scale: float = 1):
        painter.draw_rectangle(x + 1, y + 1, self.width - 2, self.height - 2)
        painter.draw_text(x + self.width / 2, y + self.height / 2, self.var_name, self.font)