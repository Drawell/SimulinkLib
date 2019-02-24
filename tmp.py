import os, sys
import importlib.util
from importlib import import_module
from environment import Environment
from env_manager import EnvManager
from SimStandardModules.SimTmp import SimTmp
from SimStandardModules.SimScope import SimScope


from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from view_widget import ViewWidget

import cairo
from io import BytesIO



class TmpWindow(QMainWindow):
    def __init__(self):
        super(TmpWindow, self).__init__(None)
        self.init_component()
        self.show()

    def init_component(self):
        self.setCentralWidget(ViewWidget(self))


        '''
        surface1 = cairo.ImageSurface(cairo.FORMAT_ARGB32, 100, 21)
        cr = cairo.Context(surface1)

        cr.set_source_rgb(0, 0, 0)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(14)
        cr.move_to(0, 20)
        cr.show_text("Hello World")

        surface2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, 60, 21)
        cr = cairo.Context(surface2)
        cr.set_source_rgb(0, 0, 0)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(14)
        cr.move_to(0, 20)
        cr.show_text("Hi!")


        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 600, 600)
        cr = cairo.Context(surface)

        x1, y1 = 0, 0
        #cr.set_source_surface(surface1, x1, y1)
        #cr.rectangle(x1, y1, 100, 21)
        #cr.fill()

        x2, y2 = 1, 1
        with BytesIO() as b:
            surface2.write_to_png(b)
            b.seek(0)
            data = b.read()

        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 120, 40)
        surf = surf.create_for_data(surface2.get_data(), cairo.FORMAT_ARGB32, 60, 20)
        #cr.scale(3, 3)
        cr.set_source_surface(surf, x2, y2)
        cr.paint()
        '''
        '''
        w = 200
        h = 200
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        cr = cairo.Context(surface)
        cr.rectangle(0, 0, w, h)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(h/6)
        name = "Scope"
        (x, y, width, height, dx, dy) = cr.text_extents(name)
        cr.move_to(w / 2 - width / 2, h - h / 16)
        cr.show_text(name)

        #cr.stroke()
        base_surface = SimScope.get_base_img_as_surface(int(w - w/4), int(h - h/4))
        cr.set_source_surface(base_surface, h/8, 0)
        cr.paint()
        '''

        '''
        w, h, name = 50, 50, 'Scope 1'
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        cr = cairo.Context(surface)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(h/6)

        # center alignment
        (x, y, width, height, dx, dy) = cr.text_extents(name)
        cr.move_to(w / 2 - width / 2, h - h / 16)
        cr.show_text(name)
        w1, h1 = int(w - w / 4), int(h - h / 4)
        base_surface = SimScope.get_base_img_as_surface(w1, h1)
        cr.set_source_surface(base_surface, w/8, 0)
        cr.paint()


        with BytesIO() as b:
            surface.write_to_png(b)
            b.seek(0)
            data = b.read()

        #s = SimScope(200, 200, name='Scope 1', width=100, height=100)
        s = SimTmp(200, 200, name='hello !', width=100, height=100)
        data = s.get_img_as_byte_data(s.width, s.height)
        '''

        env = Environment()

        for i in range(5):
            name = 'hello %s' % i
            s = SimTmp(50 + i * 70, 200, name=name)
            env.add_element(s)

        data = env.get_img_as_byte_data()

        im = QImage.fromData(data)

        s = SimTmp(50, 50, name='ads')
        env.add_element(s)

        data = env.get_img_as_byte_data()
        im = QImage.fromData(data)

        #pm = QPixmap.fromImage(data)#QPixmap(os.path.join(os.path.dirname(__file__), 'SimStandardModules', 'Images', 'simsimsim.png'))
        self.centralWidget().draw_pixmap(QPixmap(im))



ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, 390, 60)
cr = cairo.Context(ims)

cr.set_source_rgb(0, 0, 0)
cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
cr.set_font_size(40)

cr.move_to(10, 50)
cr.show_text("Hello World")

def display_cairo_surface(surface):
    """Displayhook function for Surfaces Images, rendered as PNG."""
    b = BytesIO()
    surface.write_to_png(b)
    b.seek(0)
    data = b.read()

    return ip_img

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TmpWindow()
    sys.exit(app.exec_())
