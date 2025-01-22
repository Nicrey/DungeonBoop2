from PySide6.QtWidgets import ( QWidget)
from PySide6.QtGui import  QImage, QPainter
from PySide6.QtCore import Qt, QPoint



class GridCanvas(QWidget):
        
    def __init__(self, parent_display=None, draw_canvas=None):
        super().__init__()
        self.parent_display = parent_display  

        self.width = 800
        self.height = 600
        # Initialize the drawing surface
        self.pixmap = QImage(800, 600, QImage.Format_ARGB32)
        self.pixmap.fill(Qt.transparent)

        self.grid_start = []
        self.draw_canvas = draw_canvas
        self.draw_canvas.register_grid(self)
        self.update_grid(16)
        

    def update_grid(self, grid_size):
        dx = 0
        dy = 0
        grid_points = []
        self.grid_start = []
        while (dx < self.width):
            dy = 0
            y_starts = []
            while(dy < self.height):
                y_starts.append(QPoint(dx, dy))
                grid_points.append(QPoint(dx, dy))
                dy += grid_size
            dx += grid_size
            self.grid_start.append(y_starts)
        self.paint_grid(grid_points)

    def paint_grid(self, grid_points):
        self.pixmap = QImage(800, 600, QImage.Format_ARGB32)
        self.pixmap.fill(Qt.transparent)
        painter = QPainter(self.pixmap)
        painter.setPen(Qt.black)
        for point in grid_points:
            painter.drawPoint(point)
