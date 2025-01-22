

from canvas.draw_tools.abstract_tool import Tool
from PySide6.QtWidgets import ( QWidget)
from PySide6.QtGui import QPainter, QPixmap, QPen, QBrush, QMouseEvent, QImage, QColor
from PySide6.QtCore import Qt, QPoint, QRect

from canvas.draw_tools.utils.draw_utils import draw_rect



class CircleInserter(Tool):
    
    circle_x = 32
    circle_y = 32

    def mouse_release(self, event):
        self.draw_circle(event.pos(), self.circle_x, self.circle_y)
        self.canvas.parent_display.canvas_changes()


    def paint(self, painter):
        painter.setOpacity(0.5)
        self.draw_circle(self.canvas.preview_position, self.circle_x, self.circle_y, True, painter=painter)
        painter.setOpacity(1.0)

    def update_options(self, options):
        self.circle_x = options[0].current_size
        self.circle_y = options[1].current_size


    def draw_circle(self, position, size, optional_size_y = None, preview=False, painter=None):
        if preview:
            pen = QPen(QColor(0,0,0,255))
            pen.setWidth(2)
            painter.setPen(pen)
        else:
            painter = QPainter(self.canvas.pixmap)
            pen = QPen(QColor(0,0,0,0))
            pen.setWidth(1)
            painter.setPen(pen)
        brush = QBrush(QColor(230,230,230,255))
        painter.setBrush(brush)
        size_y = size if optional_size_y is None else optional_size_y
        rect_top_left = position - QPoint(size // 2, size_y // 2)
        rect = QRect(rect_top_left.x(), rect_top_left.y(),size, size_y)
        painter.drawEllipse(rect)  
