from PySide6.QtWidgets import ( QWidget)
from PySide6.QtGui import QPainter, QPixmap, QPen, QBrush, QMouseEvent, QImage, QColor
from PySide6.QtCore import Qt, QPoint, QRect

def draw_rect(canvas, position, size, optional_size_y = None, preview=False, painter=None):
    if not painter:
        painter = QPainter(canvas.pixmap)
    if preview:
        pen = QPen(QColor(0,0,0,255))
        pen.setWidth(2)
        painter.setPen(pen)
    else:
        pen = QPen(QColor(0,0,0,0))
        pen.setWidth(1)
        painter.setPen(pen)
    brush = QBrush(QColor(230,230,230,255))
    painter.setBrush(brush)
    size_y = size if optional_size_y is None else optional_size_y
    rect_top_left = position - QPoint(size // 2, size_y // 2)
    rect = QRect(rect_top_left.x(), rect_top_left.y(),size, size_y)
    painter.drawRect(rect)  
    if not preview:
        painter.end()