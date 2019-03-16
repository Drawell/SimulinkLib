from SimPainter.sim_painter import SimPainter
import cairo
from io import BytesIO
import time

class SimCairoPainter(SimPainter):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.cr = cairo.Context(self.surface)
        self.cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

    def draw_rectangle(self, x: float, y: float, w: float, h: float):
        self.cr.rectangle(x, y, w, h)
        self.cr.stroke()

    def draw_line(self, x1: float, y1: float, x2: float, y2: float):
        self.cr.move_to(x1, y1)
        self.cr.line_to(x2, y2)
        self.cr.stroke()

    def draw_text(self, x: float, y: float, text: str, font_size: int):
        self.cr.set_font_size(font_size)
        self.cr.move_to(x, y)
        self.cr.show_text(text)
        self.cr.stroke()

    def draw_curve(self, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float):
        self.cr.move_to(x1, y1)
        self.cr.curve_to(x2, y2, x3, y3, x4, y4)
        self.cr.stroke()

    def clear(self):
        self.cr.set_source_rgb(255,255,255)
        self.cr.paint()
        self.cr.set_source_rgb(0,0,0)

    def resize(self, width: int, height: int):
        new_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.cr = cairo.Context(new_surface)
        self.cr.set_source_surface(self.surface, 0, 0)
        self.cr.paint()
        self.surface = new_surface

    def get_image_as_surface(self):
        return self.surface

    def get_image_as_byte_data(self):
        t = time.time()
        with BytesIO() as b:
            self.surface.write_to_png(b)
            b.seek(0)
            data = b.read()

        print("convert surface to byte data; w= %s, h= %s; time= %.5f" %
              (self.surface.get_width(), self.surface.get_height(), time.time() - t))

        return data