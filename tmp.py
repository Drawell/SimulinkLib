import sys
import cairo
from io import BytesIO
from abc import abstractmethod
from enum import Enum

from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt
from PyQtGUI.view_widget import ViewWidget

from Environment.environment import Environment
from SimStandardModules.SimTmp import SimTmp
from SimStandardModules.SimScope import SimScope
from SimPainter.cairo_painter import SimCairoPainter

class V(QWidget):
    def __init__(self, parent, canvas):
        super(V, self).__init__(parent)
        self.show()

class TmpWindow(QMainWindow):
    def __init__(self):
        super(TmpWindow, self).__init__(None)
        self.resize(500, 500)
        self.init_component()
        self.show()
        self.update()
        self.centralWidget().show()

    def init_component(self):
        self.env = Environment(200, 200)

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

        self.cairo_painter = SimCairoPainter(200, 200)

        s = SimTmp(50, 50, name="Name")
        self.env.add_element(s)
        self.env.paint(self.cairo_painter)
        self.im = QImage.fromData(self.cairo_painter.get_image_as_byte_data())


    def paintEvent(self, *args, **kwargs):
        p = QPainter(self)
        #p.drawPixmap(0,0, )
        p.drawImage(0,0, self.im)
        '''
        self.painter.begin(self.view_widget)
        self.painter.drawPixmap(0,0, self.canvas)
        self.painter.end()
        '''

class A:
    pass

class B(A):
    pass

b = B()
print(issubclass(type(b), A))

class En(Enum):
    a=False
    b=True
    c=False

q = En.a
if q:
    print('qwer')
else:
    print("no")
def main():
    app = QApplication(sys.argv)
    window = TmpWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    pass

"""
1) Нормальный импорт модулей
2) дирректория дирректории файла
3) get_base_img_as_byte_data

"""