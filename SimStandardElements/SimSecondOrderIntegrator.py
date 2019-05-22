from PySimCore import SimBaseClass, paint_func, sim_property, SimPainter


class SimSecondOrderIntegrator(SimBaseClass):
    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x, y, kwargs)
        self.u_socket = self.new_input_socket()
        self.x_socket = self.new_output_socket()
        self.dx_socket = self.new_output_socket()

        self.pre_u = 0
        self.pre_x = self.pre_u
        self.pre_dx = self.pre_u
        self.pre_time = 0
        self.bool_first_step = True
        self.values = []

    def update(self, new_properties: dict):
        if 'start_value' not in new_properties:  # значение по умолчанию
            self.start_value = 0
        else:
            self.start_value = float(new_properties['start_value'])

        if 'dx_const' not in new_properties:
            self.dx_const = 0
        else:
            self.dx_const = float(new_properties['dx_const'])

        if 'x_const' not in new_properties:
            self.x_const = 0
        else:
            self.x_const = float(new_properties['x_const'])

    @sim_property
    def start_value(self):
        pass

    @sim_property
    def dx_const(self):
        pass

    @sim_property
    def x_const(self):
        pass

    @staticmethod
    def get_name()->str:
        return 'Integrator. Second Order'

    def check(self, context: dict) -> dict:
        self.u_socket.set_checked(True)
        return super().check(context)

    def resize(self, w: int, h: int):
        super().resize(max(w, 80), h)

    def init_simulation(self, context):
        self.pre_u = self.start_value
        self.bool_first_step = True
        self.pre_time = 0
        self.pre_dx = self.dx_const
        self.pre_x = self.x_const

    def iterate(self, time: float, context):
        dt = time - self.pre_time
        self.pre_time = time

        if self.bool_first_step:
            if self.u_socket.get_value() is None:
                self.pre_u = self.start_value
            else:
                self.pre_u = self.u_socket.get_value()

            self.dx_socket.put_value(self.pre_dx)
            self.x_socket.put_value(self.pre_x)
            self.bool_first_step = False
            return

        u = self.u_socket.get_value()

        dx = self.pre_dx + (u + self.pre_u) / 2 * dt
        x = self.pre_x + (dx + self.pre_dx) / 2 * dt

        self.pre_u = u
        self.pre_dx = dx
        self.pre_x = x

        self.dx_socket.put_value(dx)
        self.x_socket.put_value(x)


    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        painter.set_pen_width(1)
        painter.draw_rectangle(x + 1, y + 1, w - 2, h - 2)
        painter.draw_text(x + w / 10, y + h * 3/5, '1/s^2', 12)

    @paint_func
    def paint(self, painter: SimPainter, x: float = 0, y: float = 0, scale: float = 1):
        painter.draw_rectangle(x + 1, y + 1, self.width - 2, self.height - 2)
        painter.draw_text(x + self.width / 2 - 25, y + self.height * 3 / 5, '1/s^2', self.font)

        painter.draw_text(x + self.u_socket.x_in_parent + 14,
                          y + self.u_socket.y_in_parent + 10, 'u', self.font)

        painter.draw_text(x + self.x_socket.x_in_parent - 14,
                          y + self.x_socket.y_in_parent + 10, 'x', self.font)

        painter.draw_text(x + self.dx_socket.x_in_parent - 14,
                          y + self.dx_socket.y_in_parent + 10, 'dx', self.font)