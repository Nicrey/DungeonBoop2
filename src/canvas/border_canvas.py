from PySide6.QtWidgets import ( QWidget)
from PySide6.QtGui import QPainter, QPixmap, QMouseEvent, QImage, QColor
from PySide6.QtCore import Qt, QPoint, QRect


from ui.toolbars.tools import DrawTool

class BorderCanvas(QWidget):

    def __init__(self, parent_display=None):
        super().__init__()
        self.drawing = False
        self.last_point = QPoint()
        self.parent_display = parent_display  # Reference to CanvasController

        # Initialize the drawing surface
        self.pixmap = QImage(800, 600, QImage.Format_ARGB32)
        self.pixmap.fill(Qt.transparent)
