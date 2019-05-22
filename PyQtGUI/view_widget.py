from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QDataStream, QIODevice, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QPainter, QDropEvent, QDragEnterEvent, QDragMoveEvent, QDragLeaveEvent, QMouseEvent

from PyQtGUI import SetPropertiesDialog

from ToolsStrategies import ToolManager
from PySimCore import ElementPartEnum as EPE, Environment
from SimPainter import SimCairoPainter, SimQtPainter

import time


# на этом виджете будем рсовать
class ViewWidget(QWidget):
    def __init__(self, parent, environment: Environment):
        super(ViewWidget, self).__init__(parent)
        self.env = environment
        self.tool = ToolManager(self.env) #.get_default_strategy(self.env)

        self.canvas = QPixmap(600, 500)  # this present size canvas
        self.canvas.fill(Qt.white)
        self.env_img = QImage()

        self.painter = QPainter(self)
        self.cairo_painter = SimCairoPainter(600, 500)
        self.qt_painter = SimQtPainter(600, 500)

        self.setMinimumSize(600, 500)
        self.resize(600, 500)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.mouse_pressed = False
        self.show()

    def change_mouse_cursor(self, part: EPE):
        if part is None or part == EPE.NONE:
            self.setCursor(Qt.ArrowCursor)
        elif part in [EPE.LEFT, EPE.RIGHT]:
            self.setCursor(Qt.SizeHorCursor)
        elif part in [EPE.TOP, EPE.BOTTOM]:
            self.setCursor(Qt.SizeVerCursor)
        elif part in [EPE.TOP_RIGHT, EPE.BOTTOM_LEFT]:
            self.setCursor(Qt.SizeBDiagCursor)
        elif part in [EPE.TOP_LEFT, EPE.BOTTOM_RIGHT]:
            self.setCursor(Qt.SizeFDiagCursor)
        elif part in [EPE.CENTER]:
            self.setCursor(Qt.SizeAllCursor)

    def resize(self, w, h):
        super(ViewWidget, self).resize(w, h)
        tmp_canvas = self.canvas
        self.canvas = QPixmap(max(self.width(), self.canvas.width()), max(self.height(), self.canvas.width()))
        self.painter.begin(self.canvas)
        self.painter.fillRect(0, 0, self.canvas.width(), self.canvas.height(), Qt.white)
        self.painter.drawPixmap(0, 0, tmp_canvas)
        self.painter.end()

        self.env.resize(w, h)
        self.cairo_painter.resize(w, h)
        self.qt_painter.resize(w, h)

    def resizeEvent(self, e):
        w = e.size().width()
        h = e.size().height()
        self.resize(w, h)

    def paintEvent(self, e):
        #drawing on widget
        if self.env.cmp.dirty:
            cairo = False
            if cairo:
                start_time = time.time()
                self.env.paint(self.cairo_painter)
                print(" %.6f - painting " % (time.time() - start_time))

                start_time = time.time()
                data = self.cairo_painter.get_image_as_byte_data()
                print(" %.6f - converting to bytes " % (time.time() - start_time))

                start_time = time.time()
                self.env_img = QImage.fromData(data)
                print(" %.6f - converting to QImage " % (time.time() - start_time))

                self.draw_image(self.env_img)
            else:
                start_time = time.time()
                self.env.paint(self.qt_painter)
                #print(" %.6f - painting " % (time.time() - start_time))
                self.draw_pixmap(self.qt_painter.get_pixmap())

            self.env.dirty = False

        p = QPainter(self)
        p.drawPixmap(0, 0, self.canvas)

    def draw_pixmap(self, pixmap: QPixmap, x: int = 0, y: int = 0):
        self.painter.begin(self.canvas)
        self.canvas.fill(Qt.white)
        self.painter.drawPixmap(x, y, pixmap)
        self.painter.end()

    def draw_image(self, img: QImage, x: int = 0, y: int = 0):
        self.painter.begin(self.canvas)
        self.canvas.fill(Qt.white)
        self.painter.drawImage(x, y, img)
        self.painter.end()

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        event.accept()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasFormat("application/x-simitemdata"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):
        if event.mimeData().hasFormat("application/x-simitemdata"):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasFormat('application/x-simitemdata'):
            item_data = event.mimeData().data('application/x-simitemdata')
            data_stream = QDataStream(item_data, QIODevice.ReadOnly)
            s = data_stream.readQString()

            self.env.add_element_by_name(s, event.pos().x(), event.pos().y())
            self.update()

            event.acceptProposedAction()
        else:
            event.ignore()

    def mousePressEvent(self, e: QMouseEvent):
        self.mouse_pressed = True
        self.tool.mouse_down(e.x(), e.y())

        self.update()

    def mouseMoveEvent(self, e: QMouseEvent):
        if self.mouse_pressed:
            self.tool.mouse_pressed_move(e.x(), e.y())
        else:
            self.tool.mouse_unpressed_move(e.x(), e.y())

        self.change_mouse_cursor(self.tool.get_element_part())
        self.update()

    def mouseReleaseEvent(self, e: QMouseEvent):
        self.mouse_pressed = False
        self.tool.mouse_up(e.x(), e.y())
        self.update()

    def mouseDoubleClickEvent(self, e: QMouseEvent):
        self.tool.mouse_double_click(e.x(), e.y())
        element = self.tool.get_element()
        if element is None:
            return

        element.show()

        self.dialog = SetPropertiesDialog(self, element)
        self.dialog.show()


