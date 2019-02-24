from sim_base_class import SimBaseClass
import os
import cairo


class SimSinWave(SimBaseClass):
    def __init__(self, x: int, y: int, amplitude: float = 0, phase: float = 0, **kwargs):
        if 'name'not in kwargs:
            kwargs['name'] = 'Sin Wave'
        super().__init__(x, y, kwargs)
        self.amplitude = amplitude
        self.phase = phase

    def make_step(self, time: float):
        pass

    @staticmethod
    def get_base_img_as_surface(w: int, h: int):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        cr = cairo.Context(surface)
        cr.set_line_width(1)
        cr.rectangle(1, 1, w - 2, h - 2)
        cr.move_to(5, h / 2)
        cr.line_to(w - 5, h / 2)
        cr.move_to(w / 5, 5)
        cr.line_to(w / 5, h - 5)
        cr.stroke()
        cr.move_to(w/5, h/2)
        cr.set_line_width(2)
        cr.curve_to(1.5*w/5, 5, 2.5*w/5, 5, 3*w/5, h / 2)
        cr.curve_to(3.5*w / 5, h - 10, 4.5*w/5, h - 10, w - 2, h / 2)
        cr.stroke()
        return surface
        pass

    @staticmethod
    def get_base_img_as_byte_data(w: int, h: int)-> bytes:
        surface = SimSinWave.get_base_img_as_surface(w, h)
        return SimBaseClass.get_data_from_surface(surface)

    @staticmethod
    def get_img_path()->str:
        return os.path.join(os.path.dirname(__file__), 'Images', 'SinWave.png') #'SimStandardModules',

    @staticmethod
    def get_name()->str:
        return 'SimSinWave'

    def get_img_as_surface(self, w: int, h: int):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        cr = cairo.Context(surface)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(h/5)

        # center alignment
        (x, y, width, height, dx, dy) = cr.text_extents(self.name)
        cr.move_to(w / 2 - width / 2, h - h / 16)
        cr.show_text(self.name)

        base_surface = SimSinWave.get_base_img_as_surface(int(w - w/4), int(h - h/4))
        cr.set_source_surface(base_surface, w/8, 0)
        cr.paint()
        return surface
