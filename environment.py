from sim_base_class import SimBaseClass
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
from typing import List

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