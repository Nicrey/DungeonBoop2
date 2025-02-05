from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QMouseEvent, QPen, QImage
from PySide6.QtCore import Qt, QPoint

import config


class AbstractCanvas(QWidget):

    def __init__(self, canvas_type, parent_display=None):
        super().__init__()
        self.canvas_type = canvas_type
        self.drawing = False
        self.last_point = QPoint()
        self.pen = QPen(Qt.black, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self.parent_display = parent_display  # Reference to CanvasDisplay

        # Initialize the drawing surface
        self.pixmap = QImage(config.WIDTH, config.HEIGHT, QImage.Format_ARGB32)
        self.pixmap.fill(Qt.transparent)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.position().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drawing:
            painter = QPainter(self.pixmap)
            painter.setPen(self.pen)

            if self.canvas_type == "draw":
                painter.drawLine(self.last_point, event.position().toPoint())
            elif self.canvas_type == "icons":
                painter.setBrush(Qt.red)
                painter.drawEllipse(event.position().toPoint(), 20, 20)
            elif self.canvas_type == "text":
                painter.setPen(Qt.blue)
                painter.drawText(event.position().toPoint(), "Sample Text")

            self.last_point = event.position().toPoint()
            self.update()
            if self.parent_display:
                self.parent_display.update_active_canvas()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            if self.parent_display:
                self.parent_display.update_active_canvas()

    def paint(self, event):
        pass

    def update_options(self):
        pass
