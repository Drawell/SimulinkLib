from abc import ABC, abstractmethod
from SimElement.element_part_enum import ElementPartEnum as EPE
from SimElement.sim_box import SimBox
from SimElement.sim_util import TextSizeHelper
from SimPainter.sim_painter import SimPainter

part_map = [[EPE.TOP_LEFT, EPE.TOP, EPE.TOP_RIGHT],
            [EPE.LEFT, EPE.CENTER, EPE.RIGHT],
            [EPE.BOTTOM_LEFT, EPE.BOTTOM, EPE.BOTTOM_RIGHT]]

'''
def paint_function(func):
    def wrapped(self, w: int, h: int, cr=None) -> cairo.ImageSurface:
        (x, y, width, height, dx, dy) = TextSizeHelper.get_text_size(self.name, self.font)
        width = int(max(w, width))
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, int(h + height + 4))
        cr = cairo.Context(surface)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(self.font)
        cr.move_to(0, h + self.font)
        cr.show_text(self.name)

        #base_surface = self.__class__.get_base_img_as_surface(w, h)  # int(w - w/4), int(h - h/4))
        #cr.set_source_surface(base_surface, 0, 0)
        #cr.paint()
        func(self, w, h, cr)
        return surface

    return wrapped
'''


class SimBaseClass(SimBox, ABC):
    def __init__(self, x: int, y: int, kwargs):
        width = kwargs['width'] if 'width' in kwargs else 50
        height = kwargs['height'] if 'height' in kwargs else 50
        super().__init__(x, y, width, height)
        self.name = kwargs['name'] if 'name' in kwargs else self.get_name()
        self.input_sockets = []
        self.font = 10

    def resize(self, w: int, h: int):
        super().resize(max(w, 32), max(h, 32))

    def move_to(self, x: int, y: int):
        super().move_to(x, y)

    @abstractmethod
    def make_step(self, time: float):
        pass

    @staticmethod
    def get_name()->str:
        pass

    @staticmethod
    @abstractmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        pass

    @abstractmethod
    def paint(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        pass

    '''
    @staticmethod
    def get_base_img_as_surface(w: int, h: int):
        pass

    @staticmethod
    def get_base_img_as_byte_data(w: int, h: int):
        pass
    
    @staticmethod
    def get_data_from_surface(surface)-> bytes:

        with BytesIO() as b:
            surface.write_to_png(b)
            b.seek(0)
            data = b.read()

        return data

    #@abstractmethod
    def get_img_as_surface(self, w: int, h: int) -> cairo.ImageSurface:
        (x, y, width, height, dx, dy) = TextSizeHelper.get_text_size(self.name, self.font)
        width = int(max(w, width))
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, int(h + height + 4))
        cr = cairo.Context(surface)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(self.font)

        cr.move_to(0, h + self.font)
        cr.show_text(self.name)

        base_surface = self.__class__.get_base_img_as_surface(w, h)  # int(w - w/4), int(h - h/4))
        cr.set_source_surface(base_surface, 0, 0)
        cr.paint()

        return surface

    def get_img_as_byte_data(self, w: int, h: int):
        surface = self.get_img_as_surface(w, h)
        return SimBaseClass.get_data_from_surface(surface)
    '''

    def in_element(self, x: int, y: int)-> EPE:
        radius = 5
        if self.x + self.width + radius < x or x < self.x - radius \
                or self.y + self.height + radius < y or y < self.y - radius:
            return EPE.NONE

        top = abs(y - self.y) < radius
        bottom = abs(y - self.y - self.height) < radius
        right = abs(x - self.x - self.width) < radius
        left = abs(x - self.x) < radius

        x = 0 if top else 2 if bottom else 1
        y = 0 if left else 2 if right else 1

        return part_map[x][y]

