from PySimCore import SimPainter
from PyQt5.QtGui import QPixmap, QPainter, QFont, QPainterPath, QPen, QColor
from PyQt5.QtCore import Qt


class SimQtPainter(SimPainter):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.canvas = QPixmap(width, height)
        self.canvas.fill(Qt.white)
        self.painter = QPainter(self.canvas)
        self.pen = QPen(Qt.black)
        self.painter.setPen(self.pen)

    def set_pen_width(self, width):
        self.pen.setWidth(width)
        self.painter.setPen(self.pen)

    def set_pen_colour(self, r: int, g: int, b: int):
        self.pen.setColor(QColor(r, g, b))
        self.painter.setPen(self.pen)

    def draw_rectangle(self, x: float, y: float, w: float, h: float):
        self.painter.drawRect(x, y, w, h)

    def draw_line(self, x1: float, y1: float, x2: float, y2: float):
        self.painter.drawLine(x1, y1, x2, y2)

    def draw_circle(self, x: float, y: float, r: float):
        self.painter.drawEllipse(x - r, y - r, 2 * r, 2 * r)

    def draw_text(self, x: float, y: float, text: str, font_size: int):
        self.painter.setFont(QFont("Sans", font_size))
        self.painter.drawText(x, y, text)

    def draw_curve(self, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float):
        curve = QPainterPath()
        curve.moveTo(x1, y1)
        curve.cubicTo(x2, y2, x3, y3, x4, y4)
        self.painter.drawPath(curve)

    def clear(self):
        self.canvas.fill(Qt.white)

    def resize(self, x, y):
        new_canvas = QPixmap(x, y)
        self.painter = QPainter(new_canvas)
        self.painter.drawPixmap(0, 0, self.canvas)
        self.canvas = new_canvas

    def get_pixmap(self):
        return self.canvas