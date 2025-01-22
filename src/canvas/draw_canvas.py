from PySide6.QtWidgets import ( QWidget)
from PySide6.QtGui import QPainter, QPixmap, QPen, QBrush, QMouseEvent, QImage, QColor
from PySide6.QtCore import Qt, QPoint, QRect


from ui.toolbars.tools import DrawTool


class DrawCanvas(QWidget):

    def __init__(self, parent_display=None):
        super().__init__()
        self.drawing = False
        self.last_point = QPoint()
        self.parent_display = parent_display  # Reference to CanvasController

        # Initialize the drawing surface
        self.pixmap = QImage(800, 600, QImage.Format_ARGB32)
        self.pixmap.fill(Qt.transparent)
        
        self.draw_size = 32 
        self.drawing = False

        self.eraser_size = 32
        self.erasing = False

        self.rect_x = 32
        self.rect_y = 32

        self.circle_x = 32
        self.circle_y = 32

        self.options = self.parent_display.controller.get_options()
        self.preview_position = None

        

    def get_tool(self):
        return self.parent_display.controller.current_tool
    
    def mousePressEvent(self, event: QMouseEvent):
        if self.get_tool() == DrawTool.SUBTRACT and event.button() == Qt.LeftButton:
            self.erasing = True
        if self.get_tool() == DrawTool.ADD and event.button() == Qt.LeftButton:
            self.drawing = True

    def mouseMoveEvent(self, event: QMouseEvent):
        # Update the cursor position for the preview
        self.preview_position = event.pos()
        self.parent_display.update()
        if self.erasing:
            self.erase()
        if self.drawing:
            painter = QPainter(self.pixmap)
            self.draw_rect(painter, event.pos(), self.draw_size)
            painter.end()


    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.get_tool() == DrawTool.SUBTRACT and event.button() == Qt.LeftButton:
            self.erasing = False
        if self.get_tool() == DrawTool.ADD and event.button() == Qt.LeftButton:
            self.drawing = False
        if self.get_tool() == DrawTool.RECT_ADD and event.button() == Qt.LeftButton:
            painter = QPainter(self.pixmap)
            self.draw_rect(painter, event.pos(), self.rect_x, self.rect_y)
            self.parent_display.update()
        if self.get_tool() == DrawTool.CIRCLE_ADD and event.button() == Qt.LeftButton:
            painter = QPainter(self.pixmap)
            self.draw_circle(painter, event.pos(), self.circle_x, self.circle_y)
            self.parent_display.update()

    def paint(self, painter):
        if self.preview_position and self.get_tool() == DrawTool.ADD:
            painter.setOpacity(0.5)  # Set transparency for the preview
            self.draw_rect(painter, self.preview_position, self.draw_size, preview=True)
            painter.setOpacity(1.0)  # Reset opacity
        if self.preview_position and self.get_tool() == DrawTool.RECT_ADD:
            painter.setOpacity(0.5)  # Set transparency for the preview
            self.draw_rect(painter, self.preview_position, self.rect_x, self.rect_y, True)
            painter.setOpacity(1.0)  # Reset opacity
        if self.preview_position and self.get_tool() == DrawTool.CIRCLE_ADD:
            painter.setOpacity(0.5)  # Set transparency for the preview
            self.draw_circle(painter, self.preview_position, self.circle_x, self.circle_y, True)
            painter.setOpacity(1.0)  # Reset opacity
        if self.preview_position and self.get_tool() == DrawTool.SUBTRACT:
            self.draw_eraser_preview(painter)


    def update_options(self):
        self.options = self.parent_display.controller.get_options()
        if self.get_tool() == DrawTool.ADD:
            self.draw_size = self.options[0].current_size
            self.erasing = False
        if self.get_tool() == DrawTool.SUBTRACT:
            self.eraser_size = self.options[0].current_size
        if self.get_tool() == DrawTool.RECT_ADD:
            self.rect_x = self.options[0].current_size
            self.rect_y = self.options[1].current_size
        if self.get_tool() == DrawTool.CIRCLE_ADD:
            self.circle_x = self.options[0].current_size
            self.circle_y = self.options[1].current_size
        
    
    ###############
    # Basic Drawing
    ###############

    def draw_rect(self, painter, position, size, optional_size_y = None, preview=False):
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

    def draw_circle(self, painter, position, size, optional_size_y = None, preview=False):
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
        painter.drawEllipse(rect)  

    ###################
    # ERASING
    ###################

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