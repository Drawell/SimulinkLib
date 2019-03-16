import cairo
from SimElement.sim_base_class import SimBaseClass
from SimElement.element_part_enum import ElementPartEnum
from SimPainter.sim_painter import SimPainter

## @package environment
#  Среда. В ней будет все
#
#

## Среда. В ней будет все
class Environment(SimBaseClass):
    def __init__(self, x: int, y: int):
        super().__init__(0, 0, {})
        self.present_elements = []
        #self.present_elements_surfaces = []
        self.target_x = 0
        self.target_y = 0

    def make_step(self, time: float):
        pass

    def move_to(self, x: int, y: int):
        super().move_to(min(x, 0), min(y, 0))

    @staticmethod
    def paint_base(painter: SimPainter, x: float = 0, y: float = 0, w: float = 32, h: float = 32):
        pass

    def paint(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        painter.clear()
        for i, element in enumerate(self.present_elements):
            element.paint(painter, self.x, self.y, scale)



    '''
    def get_img_as_surface(self, w: int = 0, h: int = 0):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        cr = cairo.Context(surface)

        start_time = time.time()
        dirty_time = time.time()
        dirty_time_sum = 0
        for i, element in enumerate(self.present_elements):
            if element.dirty or self.present_elements_surfaces[i] is None:
                self.present_elements_surfaces[i] = element.get_img_as_surface(element.width, element.height)
                element.dirty = False
                dirty_time_sum += time.time() - dirty_time
                dirty_time = time.time()

            element_surface = self.present_elements_surfaces[i]
            cr.set_source_surface(element_surface, element.x, element.y)
            cr.paint()
        second_time = time.time()

        targeted_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        cr = cairo.Context(targeted_surface)
        cr.set_source_surface(surface, self.x, self.y)
        cr.paint()
        print(" %.4f element | --- %.4f dirty | --- %.4f surfaces " %
              (time.time() - start_time, dirty_time_sum, time.time() - second_time))

        return targeted_surface
            
    def get_img_as_byte_data(self, w: int = 0, h: int = 0):
        surface = self.get_img_as_surface(self.width, self.height)
        return SimBaseClass.get_data_from_surface(surface)
    '''

    def add_element(self, element: SimBaseClass):
        self.present_elements.append(element)
        self.width = max(element.x + element.width, self.width)
        self.height = max(element.y + element.height, self.height)
        self.dirty = True

    def get_element_by_coord(self, x, y):
        for element in self.present_elements:
            part = element.in_element(x - self.x, y - self.y)
            if part != ElementPartEnum.NONE:
                return element, part

            # check for sockets
        return None, None