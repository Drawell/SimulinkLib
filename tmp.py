import sys
import cairo
from io import BytesIO
from abc import abstractmethod

from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt
from PyQtGUI.view_widget import ViewWidget

from Environment.environment import Environment
from SimStandardModules.SimTmp import SimTmp
from SimStandardModules.SimScope import SimScope
from SimPainter.cairo_painter import CairoPainter

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

        self.cairo_painter = CairoPainter(200, 200)

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

class Soket:
    def __init__(self, name):
        self.name = name

    def print(self):
        print(self.name)

class SockDec:
    def __init__(self, function):
        self.function = function
        self.arr = []

    def __call__(self, *params):
        self.function(params)
        self.arr.append(1)

@SockDec
def func(*params):
    print("i am func")

@SockDec
def f2(*params):
    print("f2")

#func()
#f2()
#f2()

class A:
    def __init__(self):
        self.a = Soket("hi")
        self.b = Soket("B socket")
        self.sockets = []
        self.value = 0

    def socket(func):
        print("socket")
        # init
        def decorator(self):
            #call
            #q.sockets.append(func(q))
            print("decorator")
            def wrapped(self):
                print(self.arr)
                func(self)

            return wrapped

        return decorator

    def socket2(arg1, arg2):
        print(arg1, arg2)
        def decorator(func):
            #q.sockets.append(func(q))
            print("decorator")
            def wrapped(self):
                print(self.arr)
                func(self)

            return wrapped

        return decorator

    @socket
    def socket_func(self):
        return self.a

    @socket2(1, 2)
    def socket_func_2(self):
        return self.b

    def print_sockets(self):
        for s in self.sockets:
            s.print()


a = A()
a.socket_func()
a.print_sockets()


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