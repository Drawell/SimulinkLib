from PySimCore import ElementPartEnum as EPE, SimPainter, sim_property
import xml.etree.ElementTree as xml


class SimBox:
    def __init__(self, x: int = 0, y: int = 0, w: int = 0, h: int = 0):
        self.properties = {}
        self.x = int(x)
        self.y = int(y)
        self.width = int(w)
        self.height = int(h)
        self.dirty = True

    @sim_property
    def x(self):
        pass

    @sim_property
    def y(self):
        pass

    @sim_property
    def width(self):
        pass

    @sim_property
    def height(self):
        pass

    def move_to(self, x: int, y: int):
        self.x = int(x)
        self.y = int(y)
        self.dirty = True

    def resize(self, w: int, h: int):
        self.width = int(w)
        self.height = int(h)
        self.dirty = True

    def paint(self, painter: SimPainter, x_indent: float = 0, y_indent: float = 0, scale: float = 1):
        pass
        #painter.draw_rectangle(x_indent, y_indent, 10, 10)

    def in_element(self, x: int, y: int) -> EPE:
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            return EPE.CENTER

        return EPE.NONE

    def save_to_xml(self, parent):
        box_xml = xml.SubElement(parent, 'SimBox')
        for key, value in self.properties.items():
            prop = xml.SubElement(box_xml, key)
            prop.text = str(value)