from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QDataStream, QIODevice, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QPainter, QDropEvent, QDragEnterEvent, QDragMoveEvent, QDragLeaveEvent, QMouseEvent

from ToolsStrategies.strategy_manager import StrategyManager
from Environment.environment import Environment
from SimElement.element_part_enum import ElementPartEnum as EPE
from SimPainter.cairo_painter import SimCairoPainter
from SimPainter.qt_painter import SimQtPainter

import time

# на этом виджете будем рсовать
class ViewWidget(QWidget):

    add_element_signal = pyqtSignal(str, int, int)

    def __init__(self, parent, env: Environment):
        super(ViewWidget, self).__init__(parent)
        self.env = env
        self.strategy_manager = StrategyManager(self.env)
        self.strategy = self.strategy_manager.get_default_strategy()

        self.canvas = QPixmap(500, 500)  # this present size canvas
        self.canvas.fill(Qt.white)
        self.env_img = QImage()

        self.painter = QPainter(self)
        self.cairo_painter = SimCairoPainter(500, 500)
        self.qt_painter = SimQtPainter(500, 500)

        self.setMinimumSize(400, 400)
        self.resize(500, 500)
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
        if self.env.dirty:
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
                print(" %.6f - painting " % (time.time() - start_time))
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
            print(s, event.pos().x(), event.pos().y())
            self.add_element_signal.emit(s, event.pos().x(), event.pos().y())
            event.acceptProposedAction()
        else:
            event.ignore()

    def mousePressEvent(self, e: QMouseEvent):
        self.mouse_pressed = True
        self.strategy, part = self.strategy_manager.get_strategy(e.x(), e.y())
        self.env.dirty = True
        self.change_mouse_cursor(part)
        self.update()

    def mouseMoveEvent(self, e: QMouseEvent):
        if self.mouse_pressed:
            self.strategy.mouse_pressed_move(e.x(), e.y())
            self.env.dirty = True
        else:
            self.change_mouse_cursor(self.strategy.mouse_unpressed_move(e.x(), e.y()))
        self.update()

    def mouseReleaseEvent(self, e: QMouseEvent):
        self.mouse_pressed = False
        self.strategy.mouse_up(e.x(), e.y())
        self.strategy = self.strategy_manager.get_default_strategy()
        self.update()
