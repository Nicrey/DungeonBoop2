from PySide6.QtWidgets import ( QWidget)
from PySide6.QtGui import QPainter, QPixmap, QMouseEvent, QImage, QColor
from PySide6.QtCore import Qt, QPoint, QRect


from ui.toolbars.tools import IconTool


class IconCanvas(QWidget):

    def __init__(self, parent_display=None):
        super().__init__()
        self.drawing = False
        self.last_point = QPoint()
        self.parent_display = parent_display  # Reference to CanvasController

        # Initialize the drawing surface
        self.pixmap = QImage(800, 600, QImage.Format_ARGB32)
        self.pixmap.fill(Qt.transparent)

        self.icon = QPixmap("../resources/icons/down.png")
        self.icon_size = 50
        
        self.eraser_size = 32
        self.erasing = False

        self.options = self.parent_display.controller.get_options()
        self.preview_position = None
        

    def get_tool(self):
        return self.parent_display.controller.current_tool
    
    def mousePressEvent(self, event: QMouseEvent):
        if self.get_tool() == IconTool.REMOVE_ICON and event.button() == Qt.LeftButton:
            self.erasing = True

    def mouseMoveEvent(self, event: QMouseEvent):
        # Update the cursor position for the preview
        self.preview_position = event.pos()
        self.parent_display.update()
        if self.erasing:
            self.erase()

    
    def leaveEvent(self, event):
        # Clear the preview when the mouse leaves the canvas
        print("LEave")
        self.preview_position = None
        self.parent_display.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.get_tool() == IconTool.ADD_ICON:
            painter = QPainter(self.pixmap)
            self.draw_icon(painter, event.pos())
            if self.parent_display:
                self.parent_display.update_active_canvas()
        
        if self.get_tool() == IconTool.REMOVE_ICON and event.button() == Qt.LeftButton:
            self.erasing = False

    def paint(self, painter):
        if self.preview_position and self.get_tool() == IconTool.ADD_ICON:
            painter.setOpacity(0.5)  # Set transparency for the preview
            self.draw_icon(painter, self.preview_position)
            painter.setOpacity(1.0)  # Reset opacity
        if self.preview_position and self.get_tool() == IconTool.REMOVE_ICON:
            self.draw_eraser_preview(painter)


    def update_options(self):
        self.options = self.parent_display.controller.get_options()
        if self.get_tool() == IconTool.ADD_ICON:
            self.icon = self.options[1].get_icon()
            self.icon_size = self.options[0].current_size
            self.erasing = False
        if self.get_tool() == IconTool.REMOVE_ICON:
            self.eraser_size = self.options[0].current_size
            
    def draw_icon(self, painter, position):
        scaled_icon = self.icon.scaled(self.icon_size, self.icon_size, Qt.KeepAspectRatio)
        position = position - QPoint(self.icon_size // 2, self.icon_size // 2)
        painter.drawPixmap(position, scaled_icon)
    
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