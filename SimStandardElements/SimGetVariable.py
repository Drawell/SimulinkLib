from PySimCore import SimBaseClass, paint_func, sim_property, SimPainter


class SimGetVariable(SimBaseClass):
    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x, y, kwargs)
        self.output = self.new_output_socket()

    @sim_property
    def variable(self):
        pass

    def update(self, new_properties: dict):
        self.variable = new_properties['variable'] if 'variable' in new_properties else 'Var'

    def get_local_variables(self)-> list:
        return [self.variable]

    @staticmethod
    def get_name()->str:
        return 'GetVariable'

    def init_simulation(self, context):
        super().init_simulation(context)

    def iterate(self, time: float, context):
        self.output.put_value(context[self.variable])

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        painter.draw_rectangle(x + 1, y + 1, w - 2, h - 2)
        painter.draw_text(x + w / 6, y + h / 2, 'GetVar', 9)

    @paint_func
    def paint(self, painter: SimPainter, x: float = 0, y: float = 0, scale: float = 1):
        painter.draw_rectangle(x + 1, y + 1, self.width - 2, self.height - 2)
        painter.draw_text(x + self.width / 2, y + self.height / 2, self.variable, self.font)