from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QDataStream, QIODevice, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QDropEvent, QDragEnterEvent, QDragMoveEvent, QDragLeaveEvent


# на этом виджете будем рсовать
class ViewWidget(QWidget):

    add_element_signal = pyqtSignal(str, int, int)

    def __init__(self, parent):
        super(ViewWidget, self).__init__(parent)
        self.show()
        self.canvas = QPixmap(500, 500)
        self.canvas.fill(Qt.white)
        self.painter = QPainter(self)
        self.setMinimumSize(400, 400)
        self.resize(500, 500)
        self.setAcceptDrops(True)

    def resize(self, w, h):
        super(ViewWidget, self).resize(w, h)
        tmp_canvas = self.canvas
        self.canvas = QPixmap(self.width(), self.height())
        self.painter.begin(self.canvas)
        self.painter.fillRect(0, 0, self.width(), self.height(), Qt.white)
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

    def draw_pixmap(self, pixmap: QPixmap):
        self.painter.begin(self.canvas)
        self.painter.drawPixmap(0, 0, pixmap)
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

        '''if (event->mimeData()->hasFormat("application/x-dnditemdata")) {
        QByteArray itemData = event->mimeData()->data("application/x-dnditemdata");
        QDataStream dataStream(&itemData, QIODevice::ReadOnly);

        QPixmap pixmap;
        QPoint offset;
        dataStream >> pixmap >> offset;

        QLabel *newIcon = new QLabel(this);
        newIcon->setPixmap(pixmap);
        newIcon->move(event->pos() - offset);
        newIcon->show();
        newIcon->setAttribute(Qt::WA_DeleteOnClose);

        if (event->source() == this) {
            event->setDropAction(Qt::MoveAction);
            event->accept();
        } else {
            event->acceptProposedAction();
        }
    } else {
        event->ignore();
    }'''