from PySide6.QtWidgets import (
    QWidget
)
from PySide6.QtGui import QPainter, QMouseEvent

from canvas.canvas_history import CanvasHistory
from ui.toolbars.tools import Mode


class CanvasController(QWidget):
    """
    Combines three canvases (draw, icon, text) to be able to show 
    them all at the same time and catch events for the active one
    Also draws inactive canvases greyed out
    """
    BORDER_INDEX = 3
    def __init__(self, controller):
        super().__init__()
        self.controller = controller 
        self.canvas_history = None
        self.canvases = []
        self.setMouseTracking(True)

    def update_layer(self):
        self.canvases = self.controller.get_current_layer().get_canvases()
        self.update()
        self.canvas_history = CanvasHistory(self.controller, self)
        self.canvas_history.trigger_all()
     
    def active_canvas_idx(self):
        return 0 if self.controller.mode == Mode.DRAW else (1 if self.controller.mode == Mode.ICON else 2)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        for index, canvas in enumerate(self.canvases):
            if index == self.active_canvas_idx() or index == self.BORDER_INDEX:
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
        self.canvases[3].blacken_near_transparent()

    def update_options(self):
        self.canvases[self.active_canvas_idx()].update_options()

    def canvas_changes(self):
        self.canvas_history.trigger()   
    
    def undo_complete(self):
        if self.active_canvas_idx() == 0:
            self.canvases[3].blacken_near_transparent()