

from canvas.draw_tools.abstract_tool import Tool
from canvas.draw_tools.utils.draw_utils import draw_rect, get_rect


from canvas.draw_tools.abstract_tool import Tool
from PySide6.QtWidgets import ( QWidget)
from PySide6.QtGui import QPainter, QPixmap, QPen, QBrush, QMouseEvent, QImage, QColor
from PySide6.QtCore import Qt, QPoint, QRect

from canvas.draw_tools.utils.draw_utils import draw_circle, get_rect


class FreehandDraw(Tool):

    drawing = False
    erasing = False
    draw_size = 32 

    def mouse_press(self, event):
        self.drawing = True

    def secondary_press(self, event):
        self.erasing = True
        
    def mouse_release(self, event):
        self.drawing = False
        self.canvas.parent_display.canvas_changes()

    def secondary_release(self, event):
        self.erasing = False
        self.canvas.parent_display.canvas_changes()
        
    def mouse_move(self, event):
        if self.drawing:
            rect = get_rect(event.pos(), self.draw_size)
            draw_rect(self.canvas, rect)
        if self.erasing:
            rect = get_rect(event.pos(), self.draw_size)
            draw_rect(self.canvas, rect, erase=True)

    def paint(self, painter):
        painter.setOpacity(0.5)
        rect = get_rect(self.canvas.preview_position, self.draw_size)
        draw_rect(self.canvas, rect, preview=True, painter=painter)
        painter.setOpacity(1.0)

    def update_options(self, options):
        self.draw_size = options[0].current_size

    def erase(self, rect):
        painter = QPainter(self.canvas.pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_Clear)  # Set clear mode
        painter.fillRect(rect, QColor(0, 0, 0, 0))  # Fill the rectangle with transparency (alpha = 0)
        painter.end()
    