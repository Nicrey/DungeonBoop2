

from canvas.draw_tools.abstract_tool import Tool
from PySide6.QtWidgets import ( QWidget)
from PySide6.QtGui import QPainter, QPixmap, QPen, QBrush, QMouseEvent, QImage, QColor
from PySide6.QtCore import Qt, QPoint, QRect

from canvas.draw_tools.utils.draw_utils import draw_rect, get_rect



class RectInserter(Tool):
    
    rect_x = 32
    rect_y = 32

    def mouse_release(self, event):
        rect = get_rect(event.pos(), self.rect_x, self.rect_y)
        draw_rect(self.canvas, rect)
        self.canvas.parent_display.canvas_changes()


    def paint(self, painter):
        painter.setOpacity(0.5)
        rect = get_rect(self.canvas.preview_position, self.rect_x, self.rect_y)
        draw_rect(self.canvas, rect, True, painter=painter)
        painter.setOpacity(1.0)

    def update_options(self, options):
        self.rect_x = options[0].current_size
        self.rect_y = options[1].current_size
