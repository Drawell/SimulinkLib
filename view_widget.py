from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QDataStream, QIODevice, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QPainter, QDropEvent, QDragEnterEvent, QDragMoveEvent, QDragLeaveEvent


# на этом виджете будем рсовать
class ViewWidget(QWidget):

    add_element_signal = pyqtSignal(str, int, int)

    def __init__(self, parent):
        super(ViewWidget, self).__init__(parent)
        self.show()
        self.canvas = QPixmap(500, 500)  # this present size canvas
        self.canvas.fill(Qt.white)
        self.present_canvas = QPixmap(500, 500)  # there is all that we could see
        self.present_canvas.fill(Qt.white)

        self.painter = QPainter(self)
        self.setMinimumSize(400, 400)
        self.resize(500, 500)
        self.setAcceptDrops(True)

    def resize(self, w, h):
        super(ViewWidget, self).resize(w, h)
        tmp_canvas = self.canvas
        self.canvas = QPixmap(max(self.width(), self.canvas.width()), max(self.height(), self.canvas.width()))
        self.painter.begin(self.canvas)
        self.painter.fillRect(0, 0, self.canvas.width(), self.canvas.height(), Qt.white)
        self.painter.drawPixmap(0, 0, tmp_canvas)
        self.painter.end()

    def resizeEvent(self, e):
        w = e.size().width()
        h = e.size().height()
        self.resize(w, h)

    def paintEvent(self, e):
        #drawing on widget
        self.painter.begin(self)
        self.painter.drawPixmap(0, 0, self.canvas)
        self.painter.end()

    def draw_pixmap(self, pixmap: QPixmap, x: int = 0, y: int = 0):
        self.painter.begin(self.canvas)
        self.canvas.fill(Qt.white)
        self.painter.drawPixmap(x, y, pixmap)
        self.painter.end()

    def draw_image(self, img: QImage, x: int = 0, y: int = 0):
        self.draw_pixmap(QPixmap(img), x, y)

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
