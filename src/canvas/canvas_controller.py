from PySide6.QtWidgets import (
    QWidget
)
from PySide6.QtGui import QPainter, QMouseEvent

from ui.toolbars.tools import Mode


class CanvasController(QWidget):
    """
    Combines three canvases (draw, icon, text) to be able to show 
    them all at the same time and catch events for the active one
    Also draws inactive canvases greyed out
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller 
        self.canvases = []
        self.setMouseTracking(True)

    def update_active_canvas(self):
        self.update()

    def update_layer(self):
        self.canvases = self.controller.get_current_layer().get_canvases()
        self.update_active_canvas()
     
    def active_canvas_idx(self):
        return 0 if self.controller.mode == Mode.DRAW else (1 if self.controller.mode == Mode.ICON else 2)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        for index, canvas in enumerate(self.canvases):
            if index == self.active_canvas_idx():
                # Draw active canvas normally
                painter.drawImage(0, 0, canvas.pixmap)
                canvas.paint(painter)
            else:
                # Grey out inactive canvases
                painter.setOpacity(0.5)  # Set transparency for inactive canvases
                painter.drawImage(0, 0, canvas.pixmap)
                painter.setOpacity(1.0)  # Reset opacity


    def mousePressEvent(self, event: QMouseEvent):
        self.canvases[self.active_canvas_idx()].mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        self.canvases[self.active_canvas_idx()].mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.canvases[self.active_canvas_idx()].mouseReleaseEvent(event)

    def update_options(self):
        self.canvases[self.active_canvas_idx()].update_options()