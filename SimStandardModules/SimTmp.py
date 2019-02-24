import os.path
from sim_base_class import SimBaseClass
import cairo
from io import BytesIO


class SimTmp(SimBaseClass):
    def __init__(self, x: int, y: int, **kwargs):
        if 'name'not in kwargs:
            kwargs['name'] = 'Hello'
        super(SimTmp, self).__init__(x, y, kwargs)

    def make_step(self, time: float):
        pass

    @staticmethod
    def get_base_img_as_surface(w: int, h: int):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        cr = cairo.Context(surface)
        cr.set_line_width(1)
        cr.rectangle(1, 1, w - 2, w - 2)
        cr.set_font_size(h*2/3)
        cr.move_to(w/10, h/2 + h / 5)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.show_text("Hi!")
        cr.stroke()
        return surface

    @staticmethod
    def get_base_img_as_byte_data(w: int, h: int):
        surface = SimTmp.get_base_img_as_surface(w, h)
        with BytesIO() as b:
            surface.write_to_png(b)
            b.seek(0)
            data = b.read()

        return data

    @staticmethod
    def get_img_path()->str:
        return os.path.join(os.path.dirname(__file__), 'Images', 'simsimsim.png')

    @staticmethod
    def get_name()->str:
        return 'SimSim'

    def get_img_as_surface(self, w: int, h: int):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        cr = cairo.Context(surface)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(h / 5)

        # center alignment
        (x, y, width, height, dx, dy) = cr.text_extents(self.name)
        cr.move_to(w / 2 - width / 2, h - h / 16)
        cr.show_text(self.name)

        base_surface = SimTmp.get_base_img_as_surface(int(w - w / 4), int(h - h / 4))
        cr.set_source_surface(base_surface, w / 8, 0)
        cr.paint()
        return surface
