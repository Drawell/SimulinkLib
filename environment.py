from sim_base_class import SimBaseClass
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
from typing import List
import cairo

## @package environment
#  Среда. В ней будет все
#
#

## Среда. В ней будет все
class Environment:
    def __init__(self):
        super().__init__()
        self.present_elements = []
        self.width = 0
        self.height = 0

    def add_element(self, element: SimBaseClass):
        self.present_elements.append(element)
        self.width = max(element.x + element.width, self.width)
        self.height = max(element.y + element.height, self.height)

    def get_img_as_surface(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        cr = cairo.Context(surface)

        for element in self.present_elements:
            element_surface = element.get_img_as_surface(element.width, element.height)
            cr.set_source_surface(element_surface, element.x, element.y)
            cr.paint()

        return surface

    def get_img_as_byte_data(self):
        surface = self.get_img_as_surface()
        return SimBaseClass.get_data_from_surface(surface)

    def draw_qpixmap(self):
        '''

        :return:
        '''
        pixmap = QPixmap(self.width, self.height)
        painter = QPainter(pixmap)
        pixmap.fill(Qt.white)

        for item in self.present_elements:
            painter.drawPixmap(item.x, item.y, QPixmap(item.get_img_path()).scaled(item.width, item.height))

        return pixmap