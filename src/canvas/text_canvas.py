from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QMouseEvent, QColor, QImage
from PySide6.QtCore import Qt, QPoint, QRect

from ui.toolbars.tools import TextTool


class TextCanvas(QWidget):

    def __init__(self, parent_display=None):
        super().__init__()
        self.parent_display = parent_display  # Reference to CanvasDisplay

        # Initialize the drawing surface
        self.pixmap = QImage(800, 600, QImage.Format_ARGB32)
        self.pixmap.fill(Qt.transparent)
        self.color = None
        self.text = ""
        self.text_size = 12

        self.eraser_size = 32
        self.erasing = False

        self.preview_position = None

    def get_tool(self):
        return self.parent_display.controller.current_tool
    
    def mousePressEvent(self, event: QMouseEvent):
        if self.get_tool() == TextTool.REMOVE_TEXT and event.button() == Qt.LeftButton:
            self.erasing = True

    def mouseMoveEvent(self, event: QMouseEvent):
        # Update the cursor position for the preview
        self.preview_position = event.pos()
        self.parent_display.update()
        if self.erasing:
            self.erase()

    
    def leaveEvent(self, event):
        # Clear the preview when the mouse leaves the canvas
        self.preview_position = None
        self.parent_display.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.get_tool() == TextTool.ADD_TEXT:
            painter = QPainter(self.pixmap)
            self.draw_text(painter, event.pos())
            self.parent_display.canvas_changes()

        if self.get_tool() == TextTool.REMOVE_TEXT and event.button() == Qt.LeftButton:
            self.erasing = False
            self.parent_display.canvas_changes()

    def paint(self, painter):
        if self.preview_position and self.get_tool() == TextTool.ADD_TEXT:
            painter.setOpacity(0.5)  # Set transparency for the preview
            self.draw_text(painter, self.preview_position)
            painter.setOpacity(1.0)  # Reset opacity
        if self.preview_position and self.get_tool() == TextTool.REMOVE_TEXT:
            self.draw_eraser_preview(painter)   


    def update_options(self):
        self.options = self.parent_display.controller.get_options()
        if self.get_tool() == TextTool.ADD_TEXT:
            self.text = self.options[3].text
            self.font = self.options[2].get_font()
            self.color = self.options[1].color
            self.text_size = self.options[0].current_size
            self.erasing = False
        if self.get_tool() == TextTool.REMOVE_TEXT:
            self.eraser_size = self.options[0].current_size
    

    def draw_text(self, painter, position):
        painter.setPen(Qt.black)
        if self.color and self.color != QColor(0,0,0, 0):
            self.color.setAlpha(255)
            painter.setPen(self.color)
        font = painter.font()
        font.setPointSize(self.text_size)
        font.setFamily(self.font)
        painter.setFont(font)
        painter.drawText(position, self.text)
    
    def erase(self):
        painter = QPainter(self.pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_Clear)  # Set clear mode
        rect_top_left = self.preview_position - QPoint(self.eraser_size // 2, self.eraser_size // 2)
        rect = QRect(rect_top_left.x(), rect_top_left.y(),self.eraser_size, self.eraser_size)
        painter.fillRect(rect, QColor(0, 0, 0, 0))  # Fill the rectangle with transparency (alpha = 0)
        painter.end()
    
    def draw_eraser_preview(self, painter):
        painter.setBrush(QColor(255, 255, 255))  # White background for the rectangle
        painter.setPen(QColor(0, 0, 0))  # Black border for the rectangle
        rect_top_left = self.preview_position - QPoint(self.eraser_size // 2, self.eraser_size // 2)
        painter.drawRect(rect_top_left.x(), rect_top_left.y(), self.eraser_size, self.eraser_size)

