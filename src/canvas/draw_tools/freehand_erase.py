

from canvas.draw_tools.abstract_tool import Tool


from canvas.draw_tools.abstract_tool import Tool
from PySide6.QtWidgets import ( QWidget)
from PySide6.QtGui import QPainter, QPixmap, QPen, QBrush, QMouseEvent, QImage, QColor
from PySide6.QtCore import Qt, QPoint, QRect

class FreehandEraser(Tool):


    erasing = False
    eraser_size = 32 

    def mouse_press(self, event):
        self.erasing = True

    def mouse_release(self, event):
        self.erasing = False
        self.canvas.parent_display.canvas_changes()

    def mouse_move(self, event):
        if self.erasing:
            self.erase()

    def paint(self, painter):
        self.draw_eraser_preview(painter)

    def update_options(self, options):
        self.eraser_size = options[0].current_size


    ###################
    # ERASING
    ###################

    def erase(self):
        painter = QPainter(self.canvas.pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_Clear)  # Set clear mode
        rect_top_left = self.canvas.preview_position - QPoint(self.eraser_size // 2, self.eraser_size // 2)
        rect = QRect(rect_top_left.x(), rect_top_left.y(),self.eraser_size, self.eraser_size)
        painter.fillRect(rect, QColor(0, 0, 0, 0))  # Fill the rectangle with transparency (alpha = 0)
        painter.end()
    
    def draw_eraser_preview(self, painter):
        painter.setBrush(QColor(255, 255, 255))  # White background for the rectangle
        painter.setPen(QColor(0, 0, 0))  # Black border for the rectangle
        rect_top_left = self.canvas.preview_position - QPoint(self.eraser_size // 2, self.eraser_size // 2)
        painter.drawRect(rect_top_left.x(), rect_top_left.y(), self.eraser_size, self.eraser_size)

