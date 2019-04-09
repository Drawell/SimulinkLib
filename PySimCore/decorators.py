#from PySimCore.sim_base_class import SimBaseClass
#from PySimCore import SimPainter


def sim_property(func):
    def set(self, value):
        self.properties[func.__name__] = value

    def get(self):
        return self.properties[func.__name__] if func.__name__ in self.properties else None

    return property(get, set)


def paint_func(func):
    #def wrapped(self: SimBaseClass, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
    def wrapped(self, painter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        painter.set_pen_width(3)
        x = self.x + x_indent
        y = self.y + y_indent
        for s in self.input_sockets_iter():
            s.paint(painter, x_indent, y_indent, scale)

        for s in self.output_sockets_iter():
            s.paint(painter, x_indent, y_indent, scale)

        painter.set_pen_width(1)
        func(self, painter, x, y, scale)

    return wrapped