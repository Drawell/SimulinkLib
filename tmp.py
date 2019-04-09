import sys

from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt

from Environment import Environment, EnvManager
from ExtraElements.SimTmp import SimTmp
from SimStandardElements.SimAdd import SimAdd
from SimStandardElements.SimConst import SimConst
from SimStandardElements.SimSetVariable import SimSetVariable

from SimPainter import SimCairoPainter, SimQtPainter


class TmpWindow(QMainWindow):
    def __init__(self):
        super(TmpWindow, self).__init__(None)
        self.resize(500, 500)
        self.init_component()
        self.show()
        self.update()
        self.centralWidget().show()

    def init_component(self):
        self.env = Environment(0, 0, 200, 200, 'a')
        self.env_manager = EnvManager(self.env)

        self.main_layout = QHBoxLayout(self)
        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(self.main_layout)

        self.view_widget = QWidget(self) #ViewWidget(self, self.env)
        self.main_layout.addWidget(self.view_widget)
        self.view_widget.setGeometry(0, 0, 500, 500)
        self.view_widget.show()


        self.canvas = QPixmap(500, 500)
        self.canvas.fill(Qt.white)


        self.painter = QPainter()

        self.cairo_painter = SimQtPainter(500, 500)#SimCairoPainter(200, 200)

        add = SimAdd(100, 100, signs='+-+')
        self.env_manager.add_element(add)
        const1 = SimConst(20, 50, value=5)
        self.env_manager.add_element(const1)
        const2 = SimConst(20, 100, value=7)
        self.env_manager.add_element(const2)
        const3 = SimConst(20, 150, value=4)
        self.env_manager.add_element(const3)

        out = SimSetVariable(200, 100, var_name='v')
        self.env_manager.add_element(out)

        print(self.env.connect(const1, const1.output, add, add.inputs[0]))
        print(self.env.connect(const2, const2.output, add, add.inputs[1]))
        print(self.env.connect(const3, const3.output, add, add.inputs[2]))
        print(self.env.connect(add, add.output, out, out.input))

        context = {}

        self.env_manager.run_simulation(0, 1, 1, context)
        print(context['v'])

        self.env.paint(self.cairo_painter)
        #self.im = QImage.fromData(self.cairo_painter.get_image_as_byte_data())
        self.px = self.cairo_painter.get_pixmap()

    def paintEvent(self, *args, **kwargs):
        p = QPainter(self)
        p.drawPixmap(0,0, self.px)
        #p.drawImage(0,0, self.im)
        '''
        self.painter.begin(self.view_widget)
        self.painter.drawPixmap(0,0, self.canvas)
        self.painter.end()
        '''

aa = {'a': [1, 2], 'b': []}
bb = {'a': [], 'b': [1]}
cc = {'a': [], 'b': []}
for key in cc.keys():
    cc[key].extend(bb[key])
    cc[key].extend(aa[key])

l = [5, 4, 3, 2, 1]
l.append(l.pop(1))

print(l)

s = '+-+-+'
for c in s:
    print(c)

'''
class A:
    def __init__(self):
        self.pr = {}

    def print(self):
        print(self.pr)

class B(A):
    def __init__(self):
        super().__init__()
        self.qwer = 'qw'

    @sim_property
    def a(self):
        pass

    @sim_property
    def qwer(self):
        pass


c = B()
c.a = 123
print(c.a)
c.a = 44
c.print()
'''

def main():
    app = QApplication(sys.argv)
    window = TmpWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    pass

"""
    1) как запилить изменение объектов при изменении типа? составной элемент
    
"""