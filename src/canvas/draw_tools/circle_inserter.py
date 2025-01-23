

from canvas.draw_tools.abstract_tool import Tool
from PySide6.QtWidgets import ( QWidget)
from PySide6.QtGui import QPainter, QPixmap, QPen, QBrush, QMouseEvent, QImage, QColor
from PySide6.QtCore import Qt, QPoint, QRect

from canvas.draw_tools.utils.draw_utils import draw_circle, get_rect




class CircleInserter(Tool):
    
    circle_x = 32
    circle_y = 32

    def mouse_release(self, event):
        rect = get_rect(event.pos(), self.circle_x, self.circle_y)
        draw_circle(self.canvas, rect)
        self.canvas.parent_display.canvas_changes()

    def paint(self, painter):
        painter.setOpacity(0.5)
        rect = get_rect(self.canvas.preview_position, self.circle_x, self.circle_y)
        draw_circle(self.canvas, rect, True, painter=painter)
        painter.setOpacity(1.0)

    def update_options(self, options):
        self.circle_x = options[0].current_size
        self.circle_y = options[1].current_size
