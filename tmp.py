import sys

from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt

from PySimCore import SimCompositeElement, Environment
from ExtraElements.SimTmp import SimTmp
from SimStandardElements.SimAdd import SimAdd
from SimStandardElements.SimConst import SimConst
from SimStandardElements.SimSetVariable import SimSetVariable

from SimPainter import SimCairoPainter, SimQtPainter
import ast

"""
class TmpWindow(QMainWindow):
    def __init__(self):
        super(TmpWindow, self).__init__(None)
        self.resize(500, 500)
        self.init_component()
        self.show()
        self.update()
        self.centralWidget().show()

    def init_component(self):
        # self.cmp = SimC(200, 200, 'a')
        self.env = Environment()

        self.main_layout = QHBoxLayout(self)
        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(self.main_layout)

        self.view_widget = QWidget(self)  # ViewWidget(self, self.env)
        self.main_layout.addWidget(self.view_widget)
        self.view_widget.setGeometry(0, 0, 500, 500)
        self.view_widget.show()

        self.canvas = QPixmap(500, 500)
        self.canvas.fill(Qt.white)

        self.painter = QPainter()

        self.cairo_painter = SimQtPainter(500, 500)  # SimCairoPainter(200, 200)

        add = SimAdd(100, 100, signs='+-+')
        self.env.add_element(add)
        const1 = SimConst(20, 50, value=5)
        self.env.add_element(const1)
        const2 = SimConst(20, 100, value=7)
        self.env.add_element(const2)
        const3 = SimConst(20, 150, value=4)
        self.env.add_element(const3)

        out = SimSetVariable(200, 100, variable='v')
        self.env.add_element(out)

        print(self.env.connect(const1, const1.output, add, add.inputs[0]))
        print(self.env.connect(const2, const2.output, add, add.inputs[1]))
        print(self.env.connect(const3, const3.output, add, add.inputs[2]))
        print(self.env.connect(add, add.output, out, out.input))

        context = {}

        self.env.run_simulation(0, 1, 1, context)
        print(context['v'])

        self.env.paint(self.cairo_painter)
        # self.im = QImage.fromData(self.cairo_painter.get_image_as_byte_data())
        self.px = self.cairo_painter.get_pixmap()

    def paintEvent(self, *args, **kwargs):
        p = QPainter(self)
        p.drawPixmap(0, 0, self.px)
        # p.drawImage(0,0, self.im)
        '''
        self.painter.begin(self.view_widget)
        self.painter.drawPixmap(0,0, self.canvas)
        self.painter.end()
        '''


# s = "[1, 2, 3, 4, 5]"
#s = "1.3"
#x = ast.literal_eval(s)
#print(x)

l1 = [1, 2, 3]
l2 = [1, 2, 4]
for i in range(len(l1) - len(l2)):
    print("i: ", i)



#
class A:
    def __init__(self):
        self.pr = {}

    def print(self):
        return 'I AM ALIVE!'


class B():
    def __init__(self, a: A):
        self.a = a

    def __str__(self):
        if self.a is None:
            return 'NOOO'
        return str(self.a.print())


def ff(a):
    del a


def fff():
    a = A()
    b = B(a)
    del a  # qew
    # ff(a) asfad

    print(b)


def main():
    app = QApplication(sys.argv)
    window = TmpWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    fff()
    main()
    pass

"""

